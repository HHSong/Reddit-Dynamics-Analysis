import treeNode as tn
from bs4 import BeautifulSoup

deleted = 'deleted'


def get_head(soup):
    return soup.find('head')


def get_category(head):
    title = head.find('title').contents[0]
    colon = title.rfind(":")
    category = title[colon+1:].lstrip()
    return category


def get_user(tag):
    try:
        author_nodes = tag.select('a[class^=author]')
        if len(author_nodes) == 0:
            return deleted
        return str(author_nodes[0].contents[0])
    except IndexError as err:
        raise RuntimeError(tag)


def get_main_scores(body):
    side = body.select_one('div[class=side]')
    link_info = side.select_one('div[class=linkinfo]')
    upvotes = link_info.select_one('span[class=upvotes]').select_one('span[class=number]').string.replace(',', '')
    downvotes = link_info.select_one('span[class=downvotes]').select_one('span[class=number]').string.replace(',', '')
    return {
        'likes': int(upvotes),
        'dislikes': int(downvotes),
        'unvoted': 0
    }


def get_scores(tag):
    likes = points_to_int(
        tag.select_one('span.score.likes').string
    )
    unvoted = points_to_int(
        tag.select_one('span.score.unvoted').string
    )
    dislikes = points_to_int(
        tag.select_one('span.score.dislikes').string
    )
    return {
        'likes': likes,
        'unvoted': unvoted,
        'dislikes': dislikes
    }


def points_to_int(points):
    index = points.index('point')
    return int(points[:index])


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
    if this == deleted:
        return deleted
    update_scores(
        this,
        get_main_scores(soup)
    )
    category = get_category(
        get_head(soup)
    )
    this.category = category
    return this


def update_scores(tree_node, scores):
    tree_node.likes = scores['likes']
    tree_node.unvoted = scores['unvoted']
    tree_node.dislikes = scores['dislikes']


def parse_comment(parent, comment_node):
    tag = get_tag_block(comment_node)
    this = init_tree_node(tag)
    if this == deleted:
        return deleted
    update_scores(
        this,
        get_scores(tag)
    )
    this.category = parent.category
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
