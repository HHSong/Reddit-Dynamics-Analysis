from functools import reduce


class TreeNode(object):
    def __init__(self):
        self.id = None
        self.user = None
        self.timestamp = None
        self.category = None
        self.likes = None
        self.unvoted = None
        self.dislikes = None
        self.children = []

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str({
            'id': self.id,
            'user': self.user,
            'category': self.category,
            'timestamp': self.timestamp,
            'likes': self.likes,
            'unvoted': self.unvoted,
            'dislikes': self.dislikes,
            'children': self.children
        })

    def non_direct_descendants(self):
        distants = list(
            map(
                lambda child: child.descendants(),
                self.children
            )
        )
        if len(distants) == 0:
            return []
        return reduce(
            lambda x, y: x + y,
            distants
        )

    def descendants(self):
        return self.children + self.non_direct_descendants()


class Edge(object):
    def __init__(self):
        self.master = None
        self.slave = None
        self.weight = None
        self.category = None
        self.timestamp = None

    def __str__(self):
        return str({
            'master': self.master,
            'slave': self.slave,
            'timestamp': self.timestamp,
            'weight': self.weight,
            'category': self.category
        })

    def __repr__(self):
        return self.__str__()
