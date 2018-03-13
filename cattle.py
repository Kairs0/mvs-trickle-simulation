#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

from node import Node

class Cattle():

    def __init__(self):
        self.nodes = set()
        self.max = 1
        self.i_min = 10
        self.k = 5

    @property
    def i_max(self):
        return self.i_min * (2 ** self.max)

    def new_node(self, name, n):
        node = Node(name=name, n=n, i=self.i_min, k=self.k, imin=self.i_min, imax=self.i_max)
        self.nodes.add(node)
        return node

    def tick(self):
        [node] = random.sample(self.nodes, 1)
        print(f"cattle: tick on node {node.name}")
        node.tick()
