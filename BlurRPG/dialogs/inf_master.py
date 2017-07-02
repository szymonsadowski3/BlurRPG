from anytree import Node, RenderTree

yn = ["Yes", "No"]

root = Node("1", content="Hello Discrete Wanderer! Tell me... Have you ever wondered about notion of Infinity?", answers=yn)

yes1 = Node("Yes", content="Well... Obviously, I have also had my meditation in this topic. Do you want to hear my conclusions?", parent=root, answers=yn)
no1 = Node("No", content="Well... Maybe you want to educate a bit in this topic?", parent=root, answers=yn)

#yes1
yes_to_yes1 = Node("Yes", content="Excellent! Please choose one from these topics. I don't have time to explore them all", parent=yes1, answers=["Nature", "Origin", "Symbol"])
no_to_yes1 = Node("No", content="Well... Maybe you are not worthy to hear about this after all... You came such a long way just to experience failure! Well, you are only some pathetic, worthless worm in the face of Infinity. In the name of Infinity I sentence you to death!", parent=yes1, answers=["What!? No!"])

#no1
yes_to_no1 = Node("Yes", content="That is great, but considering you have not done any contemplation in this field I can only teach you some simpler things. Choose one from them", parent=no1, answers=["Basics", "Symbol"])
no_to_no1 = Node("No", content="Just what I thought about you! You do not even express your desire to enchance knowledge in this most important topic of all possible! I don't know if you even deserve to die. Just go away, you little worm!", parent=no1, answers=["What!? No!"])

#yes1 -> yes
nature = Node("Nature", content="So you want to learn more about nature of Infinity. This is very difficult to discuss. Some claim that Infinity exist only in ones' minds. This is pure heresy! The Infinity is real! It Reason-For-Everything, Prime Mover. We are all only helpless worms, who should bend knees in face of the Infinity and hope for mercy...", parent=yes_to_yes1, answers=["You are completely insane."])
origin = Node("Origin", content="To be honest, it is impossible to learn the Origin of Infinity, because Infinity is overall origin of everything itself. To be precise, we can say that it has no origin.", answers=["You are completely insane."])
symbol = Node("Symbol", content="This is one of easier topics to discuss. The symbol of Infinity (well-known fallen 8) is representation of Uroboros - serpenteating its own tail. It is a great depiction, as wandering forward from randomly-picked point on symbol, you end up wandering endlessly.", parent=yes_to_yes1, answers=["You are completely insane."])

#no1 -> yes
basics = Node("Basics", content="Infinity is basically the Great Force, Prime Mover, Origin of Everything. You cannot see it, yet you can without hesitation claim it is perfect. It is full of paradoxes, yet full of logic. It is beautiful. ", answers=["You are completely insane."])
symbol = Node("Symbol", content="This is one of easier topics to discuss. The symbol of Infinity (well-known fallen 8) is representation of Uroboros - serpenteating its own tail. It is a great depiction, as wandering forward from randomly-picked point on symbol, you end up wandering endlessly.", parent=yes_to_yes1, answers=["You are completely insane."])

class DisplayConversation(object):
    def __init__(self, root):
        self.root = root

    def run(self):
        curr_node = self.root
        while True:
            print(curr_node.content, ' | ', curr_node.answers)
            user_input = input('Type in answer: ').strip()

            for node in curr_node.children:
                if node.name == user_input:
                    curr_node = node

DisplayConversation(root).run()
