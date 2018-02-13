from functools import reduce

class TreeNode(object):
  def __init__(self):
    self.data = None
    self.id = None
    self.user = None
    self.timestamp = None
    self.children = []

  def __repr__(self):
    return self.__str__()

  def __str__(self):
    return str({
      'id': self.id,
      'user': self.user,
      'timestamp': self.timestamp,
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