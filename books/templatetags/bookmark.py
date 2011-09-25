#encoding=utf-8
from django import template
from books.models import Bookmark
register = template.Library()

# Node
class IfBookmarkNode(template.Node):
    def __init__(self, user, book, nodelist_true, nodelist_false):
        self.user = template.Variable(user)
        self.book = template.Variable(book)
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false

    def render(self, context):
        try:
            user = self.user.resolve(context)
            book = self.book.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        # if else
        if Bookmark.objects.filter(user__pk=user.id,
                                   book__pk=book.id):
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)



# tag 
@register.tag(name='if_bookmarked')
def do_if_bookmarked(parser, token):
    try:
        tag_name, user, book = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires two argument" % token.contents.split()[0]

    nodelist_true = parser.parse(('else_bookmarked', 'endif_bookmarked')) 
    token = parser.next_token()
    if token.contents == 'else_bookmarked':
        nodelist_false = parser.parse(('endif_bookmarked',))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()
    
    return IfBookmarkNode(user, book, nodelist_true, nodelist_false)
