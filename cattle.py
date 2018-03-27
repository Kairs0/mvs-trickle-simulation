#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
import logging

from node import Node

logging.basicConfig(filename='network.log', level=logging.INFO)


class Cattle:

    def __init__(self):
        self.nodes = set()
        self.max = 5
        self.i_min = 10
        self.k = 5
        self.time = 0
        self.connected_nodes = set()

    @property
    def current_version(self):
        v = 0
        for node in self.nodes:
            if node.n > v:
                v = node.n
        return v

    @property
    def min_version(self):
        v = 0
        for node in self.nodes:
            if node.n < v:
                v = node.n
        return v

    @property
    def coverage(self):
        total_nodes = len(self.nodes)
        current_version = self.current_version
        number_updated = len([node for node in self.nodes if node.n == current_version])
        return float(number_updated) / float(total_nodes)

    @property
    def i_max(self):
        return self.i_min * (2 ** self.max)

    def new_node(self, name, n, connected=False):
        node = Node(name=name, n=n, i=self.i_min, k=self.k, imin=self.i_min, imax=self.i_max)
        self.nodes.add(node)
        logging.debug(f"Added node {node.name}")
        logging.info(f"Added node {node.name}")
        if connected:
            self.connected_nodes.add(node)
        return node

    def remove_node(self, node=None, name=None):
        if not node and not name:
            raise ValueError("Must specify either a node or a name")
        if node:
            self.nodes.discard(node)
            self.connected_nodes.discard(node)
        elif name:
            self.nodes.discard(self.get_node_by_name(name))
            self.connected_nodes.discard(self.get_node_by_name(name))

    def tick(self):
        self.time += 1
        [node] = random.sample(self.nodes, 1)
        message = f"cattle: t={self.time} tick on node" \
                  f" {node.name} (n={node.n}, t={node.t}, I={node.i}, tau={node.tau})\n" + \
                  "Versions: " + str({node.name: node.n for node in self.nodes}) + "\n" + \
                  f"coverage for version {self.current_version} : {self.coverage * 100} %"

        logging.debug(message)
        logging.info(message)

        min_v = self.min_version

        node.tick()

        if self.coverage == 1:
            logging.debug(f"Coverage complete for {self.current_version} obtained at {self.time} with "
                  f"{self.get_number_of_code_sendings()} messages sent")
            logging.info(f"Coverage complete for {self.current_version} obtained at {self.time} with "
                          f"{self.get_number_of_code_sendings()} messages sent")
        if self.min_version > min_v:
            logging.debug(f"node {node.name} is the last one to update from version {min_v} to {self.min_version}")
            logging.info(f"node {node.name} is the last one to update from version {min_v} to {self.min_version}")

    def get_node_by_name(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None

    def start(self, sleep=0):
        logging.debug("Started")
        logging.info("Started")
        while True:
            self.tick()
            time.sleep(sleep)

    def get_versions(self):
        return {node.name: node.n for node in self.nodes}

    def get_number_of_code_sendings(self):
        return sum([node.number_of_sent_messages for node in self.nodes])
