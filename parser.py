import treeNode as tn
from bs4 import BeautifulSoup

deleted = 'deleted'

def get_user(tag):
    try:
      author_nodes = tag.select('a[class^=author]')
      if len(author_nodes) == 0:
          return deleted
      return str(author_nodes[0].contents[0])
    except IndexError as err:
        raise RuntimeError(tag)

def get_timestamp(tag):
  return tag.find('time')['title']

def get_comment_area(soup):
  return soup.find('body').select('div[class^=commentarea]')[0]

def get_tag_block(soup):
  return soup.select('p[class^=tagline]')[0]

def get_comments(sitetable_parent):
  sitetables = sitetable_parent.select('div[class$=listing]')
  if len(sitetables) == 0:
      return []
  comments = list(
    filter(
      lambda div: 'thing' in div['class'], 
      sitetables[0].children
      )
    )
  return comments


def get_children(comment):
  return get_comments(comment)


def init_tree_node(tag):
  user = get_user(tag)
  if user == deleted:
    return deleted
  timestamp = get_timestamp(tag)
  this = tn.TreeNode()
  this.user = user
  this.timestamp = timestamp
  return this

def parse_post_entry(soup):
  main_entry = soup.select('div[class^=content]')[0].select('div[class^=entry]')[0]
  tag = get_tag_block(main_entry)
  this = init_tree_node(tag)
  return this

def parse_comment(parent, comment_node):
  tag = get_tag_block(comment_node)
  this = init_tree_node(tag)
  if this == deleted:
    return deleted
  parent.children.append(this)
  parse_children(this, comment_node)
  

def parse_children(this, comment_node):
  children = get_children(comment_node)
  for child in children:
    parse_comment(this, child)

def parse_comment_area(root, commentarea):
  comments = get_comments(commentarea)
  for comment in comments:
    parse_comment(root, comment)


def parse(filename):
  with open(filename) as fp:
    soup = BeautifulSoup(fp, "lxml")

    # main post
    post = parse_post_entry(soup)
    if post == deleted:
      fp.close()
      return deleted

    # comment section
    commentarea = get_comment_area(soup)
    parse_comment_area(post, commentarea)

  soup.decompose()
  fp.close()
  return post