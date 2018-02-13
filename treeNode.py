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
