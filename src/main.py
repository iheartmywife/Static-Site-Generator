from textnode import TextNode, TextType

def main():
    my_text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    
    print("hello world")
    print(my_text_node)


main()