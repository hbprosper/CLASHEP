# ---------------------------------------------------------------------------
# File: bdtutil.py
# Description: A wrappper for scikit-learn binary BDT classifiers.
# Created: October 2022 Harrison B. Prosper (resurrection of some BDT code
#                       I wrote way back when!)
#                       Adapted for ASP 2022, South Africa
# ---------------------------------------------------------------------------
import re
import numpy as np
import pandas as pd
import matplotlib as mp
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_text
from sys import exit
from pprint import PrettyPrinter
from copy import deepcopy
# ---------------------------------------------------------------------------
RED    ="\x1b[0;31;48m"
GREEN  ="\x1b[0;32;48m"
YELLOW ="\x1b[0;33;48m"
BLUE   ="\x1b[0;34;48m"
MAGENTA="\x1b[0;35;48m"
CYAN   ="\x1b[0;36;48m"

BOLDRED    ="\x1b[1;31;48m"
BOLDGREEN  ="\x1b[1;32;48m"
BOLDYELLOW ="\x1b[1;33;48m"
BOLDBLUE   ="\x1b[1;34;48m"
BOLDMAGENTA="\x1b[1;35;48m"
BOLDCYAN   ="\x1b[1;36;48m"
RESETCOLOR ="\x1b[0m"    # reset to default foreground color
# ---------------------------------------------------------------------------
class TreeDecoder:
    '''
    A class to map a scikit-learn DecisionTreeClassifier into a recursively
    nested Python list that models the tree.

    atree = bdt.estimators_[0]

    t = TreeDecoder(atree, names)

'''
    def __init__(self, atree, names, debug=False, maxdepth=100):
        '''
        atree    a scikit-learn DecisionTreeClassifier
        names    list of variables names
'''
        self.tree  = atree
        self.names = names
        
        # Algorithm: decode string describing tree
        # This is a bit risky because the scikit-learn 
        # format is not guaranteed to remain backwards 
        # compatible.
        self.rules  = export_text(atree,
                                  max_depth=maxdepth,
                                  decimals=5,
                                  show_weights=True,
                                  feature_names=names)
        self.debug  = debug
        self.maxdepth = maxdepth
        
        if debug:
            print(self.rules)
        
        # insert "#" to denote start of line and
        # replace "|" by "/" and \n by "@" to simplify
        # regular expressions (regex)
        
        recs = self.rules.split('\n')
        recs = ['#%s@' % x for x in recs]
        self.rules = ''.join(recs)
        self.rules = self.rules.replace('|', '/')

        # regex to pick out a line: '# .... @'
        
        self.line  = re.compile(r'#.*?@')

        # regex to pick out a leaf in decision tree
        
        self.leaf  = re.compile('^#[/ -]+?weights.+?class.+@')

        # regex to extract all numbers from string
        
        self.number= re.compile('[-]?[0-9]+[.]?[0-9]*')
        
        # initialize tree
        
        self.tree  = []

        # map to scikit-learn printout to a nested Python list
        
        self.decode_(self.tree, self.rules)
        
    def decode_(self, parent, rules, which='ROOT', depth=0):
        
        debug = self.debug
        
        if depth == 0:
            pass
            
        elif depth > self.maxdepth:
            return
        
        depth += 1
        tab  = '--'*depth
        
        # find first line in rules, which defines parent node
        
        t = self.line.match(rules)
        if t == None:
            raise ValueError('** no match in \n%s\n' % rules)
        
        node = t[0] # node is string containing variable name and cut value
        
        if debug:
            print('\n%s%s NODE( %s )\n' % (tab, which, node))
            print('%s%s RULES( %s )\n' % (tab, which, rules))

        # strip away first line from rules
        
        _, rules = rules.split(node)

        # find line in rules that divides current node into a "left"
        # and "right" node.
        # LEFT  nodes have variable <= cut value
        # RIGHT nodes have variable >  cut value
        
        cmd = r'%s.*?@' % node.split('<=')[0]
        if debug:
            print('%s%sCMD( %s )' % (tab, which, cmd))
            
        cmd = re.compile(cmd)
        t   = cmd.findall(rules)
        if len(t) == 0:
            raise ValueError('** no match in \nRULES( %s )\n' % rules)

        # split rules into left and right parts
        
        left, right = rules.split(t[0])
        if debug:
            print('%sLEFT( %s )\n' % (tab, left))
            print('%sRIGHT( %s )' % (tab, right))

        # get variable name and cut value
        _, node = node[:-1].split('---')
        name, _, value = node.split()
        value = float(value)

        # fill out parent node
        parent.append(which)
        parent.append(name),
        parent.append(value)
        parent.append([]) # left child
        parent.append([]) # right child

        # look for a LEFT leaf
        
        if self.leaf.match(left) == None:
            # no leaf found so continue climbing tree recursively
            # by passing left child to decode_
            self.decode_(parent[-2], left, 'LEFT', depth)
            
        else:
            # found a LEFT leaf

            t = self.number.findall(left)
            if len(t) != 3:
                raise ValueError("can't extract numbers from \n%s\n" % left)

            # bweight: background fraction relative to sample size
            # sweight: signal fraction relative to sample size
            # value:   -1 or +1 for original AdaBoost algorithm
            
            bweight, sweight, value = [float(x) for x in t]
            
            if debug:
                print('%sLEAF( %s )' % (tab, t))
                
            # update leaf info
            parent[-2].append('LEFT')
            parent[-2].append('LEAF')
            parent[-2].append(bweight)
            parent[-2].append(sweight)
            parent[-2].append(value)

        # look for a RIGHT leaf
        
        if self.leaf.match(right) == None:
            # no leaf found so continue climbing tree to the right
            self.decode_(parent[-1], right, 'RIGHT', depth)
        else:
            # found a RIGHT leaf; get its value

            t = self.number.findall(right)
            if len(t) != 3:
                raise ValueError("can't extract numbers from \n%s\n" % left)
            
            bweight, sweight, value = [float(x) for x in t]

            if debug:
                print('%sLEAF( %s )' % (tab, t))
                
            # update leaf

            parent[-1].append('RIGHT')
            parent[-1].append('LEAF')
            parent[-1].append(bweight)
            parent[-1].append(sweight)
            parent[-1].append(value)
# ---------------------------------------------------------------------------
class BDT:
    
    def __init__(self, bdt):        

        self.pp      = PrettyPrinter()
        self.trees   = bdt.estimators_
        self.weights = bdt.estimator_weights_
        self.names   = list(bdt.feature_names_in_)
        
        self.forest  = []
        for t in self.trees:
            a = TreeDecoder(t, self.names)
            self.forest.append(deepcopy(a.tree))
          
    def __del__(self):
        pass

    def decision_function(self, x, numTrees=-1, like_scikit_learn=False):
        
        if like_scikit_learn:
            weight = self.weights.sum()
        else:
            weight = 1
            
        totalTrees = len(self.forest)
        if numTrees > 0:
            ntrees = min(numTrees, totalTrees)
        else:
            ntrees = totalTrees
            
        try:
            nrows = len(x)
        except:
            nrows = 1
        
        is_dataframe = type(x) == type(pd.DataFrame)
            
        # loop over each item in x
        results = []
        for n in range(nrows):
                
            # loop over forest
            decision = 0.0
            bailout  = 500
            for itree in range(ntrees):
                
                # climb tree 
                node = self.forest[itree]
                ii = 0
                while 1:
                    ii += 1
                    if ii >= bailout:
                        raise ValueError('* lost in forest!')
                
                    name = node[1]
                
                    if name == 'LEAF':
                        leaf_value = node[-1]
                        decision += self.weights[itree] * leaf_value
                        break

                    # this is not a leaf so continue climb
                    _, name, cutvalue, left, right = node

                    # decide whether to branch "left" or "right"
                    if nrows == 1:
                        value = x[name]
                    else:
                        value = x[name].iloc[n]    
                    value = float(value)
                    
                    if value <= cutvalue:
                        node = left
                    else:
                        node = right
                        
            results.append(decision / weight)
  
        if len(results) > 1:
            return np.array(results)
        else:
            return results[0]

    def predict_proba(self, x, numTrees=-1, like_scikit_learn=False):
        f = self.decision_function(x, numTrees, like_scikit_learn)
        return 1 / (1 + np.exp(-f))
    
    def printTree(self, itree, 
                  node=None, depth=0):

        if depth == 0:
            node = self.forest[itree]
            print("\ntree number %d\tweight = %10.3e" % \
              (itree, self.weights[itree]))

        name = node[1]
        
        if name == 'LEAF':
            which, _, bweight, sweight, value = node
            signal = '%sSIG%s' % (BOLDBLUE, RESETCOLOR)
            backgd = '%sBKG%s' % (BOLDRED,  RESETCOLOR)
            name = signal if value > 0 else backgd
            print("  %s %-5s %10s %10.2e %10.2e %10.2f" % (depth*'--', 
                                            which, 
                                            name,
                                            bweight,
                                            sweight,
                                            value))

        elif len(node) == 5:
            which, name, value, left, right = node

            print("  %s %-5s %10s %10.2f" % (depth*'--', 
                                            which, 
                                            name, 
                                            value))
            depth += 1
            self.printTree(itree, left,  depth)
            self.printTree(itree, right, depth)
        else:
            raise ValueError('tree %d; wrong node length %d' % \
                            (itree, len(node)))

    def weight(self, itree):
        if itree >=0 and itree < len(self.weights):
            return self.weights[itree]
        else:
            return -1

    def plot2D(self, itree, ax,
                   fig=None,
                   useValue=False,
                   alpha=0.6,
                   edgecolor='black',
                   colormap=mp.cm.Blues):
        
        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()

        self.plot2D_(itree, xmin, xmax, ymin, ymax, useValue)
        
        patches = []
        for i in range(len(self.points)):
            patches.append( Polygon(self.points[i], closed=True) )

        colors = np.array(self.values)
        p = PatchCollection(patches,
                                cmap=colormap,
                                alpha=alpha,
                                edgecolor=edgecolor)
        p.set_array(colors)
        ax.add_collection(p)

        if fig:
            fig.colorbar(p, ax=ax)

    def plot2D_(self, itree, 
                xmin, xmax, ymin, ymax, 
                useValue,
                node=None,
                depth=0):
        
        if node == None:
            self.points = []
            self.purity = []
            self.values = []
            node = self.forest[itree]
            
        depth += 1
        if depth > 1000:
            raise ValueError('* lost deep, deep, in the forest!')
        
        name = node[1]
        
        if name == 'LEAF':
            _, _, bweight, sweight, value = node
            try:
                purity = sweight / (sweight + bweight)
            except:
                purity = 0

            points = [(xmin, ymin), (xmin, ymax),
                      (xmax, ymax), (xmax, ymin)]
                
            self.points.append(points)
            self.purity.append(purity)
            
            if useValue:
                wgt = value        
            else:
                wgt = purity
                
            self.values.append(wgt)
            return
            
        elif len(node) == 5:
            which, name, value, left, right = node

        else:
            raise ValueError('** tree %d; wrong node length %d' % \
                            (itree, len(node)))

        # there are more splits
        x_axis = name == self.names[0]
        
        if x_axis:
            # left
            xmax1= xmax
            xmax = value
            self.plot2D_(itree, xmin, xmax, ymin, ymax, useValue, left, depth)

            # right
            xmax = xmax1
            xmin = value
            self.plot2D_(itree, xmin, xmax, ymin, ymax, useValue, right, depth)

        else:
            # left
            ymax1 = ymax
            ymax = value
            self.plot2D_(itree, xmin, xmax, ymin, ymax, useValue, left, depth)

            # right
            ymax = ymax1
            ymin = value
            self.plot2D_(itree, xmin, xmax, ymin, ymax, useValue, right, depth)
            
        return
