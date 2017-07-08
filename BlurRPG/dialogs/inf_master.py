from anytree import Node, RenderTree
import Events
import Utilities as Util

yn = ["Yes", "No"]

inf_root = Node("1", content="Hello Discrete Wanderer! Tell me... Have you ever wondered about notion of Infinity?", answers=yn)

yes1 = Node("Yes", content="Well... Obviously, I have also had my meditation in this topic. Do you want to hear my conclusions?", parent=inf_root, answers=yn)
no1 = Node("No", content="Well... Maybe you want to educate a bit in this topic?", parent=inf_root, answers=yn)

#yes1
yes_to_yes1 = Node("Yes", content="Excellent! Please choose one from these topics. I don't have time to explore them all", parent=yes1, answers=["Nature", "Origin", "Symbol"])
no_to_yes1 = Node("No", content="Well... Maybe you are not worthy to hear about this after all... You came such a long way just to experience failure! Well, you are only some pathetic, worthless worm in the face of Infinity. In the name of Infinity I sentence you to death!", parent=yes1, answers=["What!? No!"], next_event=Events.PhantomGuardianBattle)

#no1
yes_to_no1 = Node("Yes", content="That is great, but considering you have not done any contemplation in this field I can only teach you some simpler things. Choose one from them", parent=no1, answers=["Basics", "Symbol"])
no_to_no1 = Node("No", content="Just what I thought about you! You do not even express your desire to enchance knowledge in this most important topic of all possible! I don't know if you even deserve to die. Just go away, you little worm!", parent=no1, answers=["What!? No!"], next_event=Events.WakeUp)

#yes1 -> yes
nature = Node("Nature", content="So you want to learn more about nature of Infinity. This is very difficult to discuss. Some claim that Infinity exist only in ones' minds. This is pure heresy! The Infinity is real! It Reason-For-Everything, Prime Mover. We are all only helpless worms, who should bend knees in face of the Infinity and hope for mercy...", parent=yes_to_yes1, answers=["You are completely insane."], next_event=Events.InfMasterDiceGame)
origin = Node("Origin", content="To be honest, it is impossible to learn the Origin of Infinity, because Infinity is overall origin of everything itself. To be precise, we can say that it has no origin.", answers=["You are completely insane."], next_event=Events.InfMasterDiceGame)
symbol = Node("Symbol", content="This is one of easier topics to discuss. The symbol of Infinity (well-known fallen 8) is representation of Uroboros - serpenteating its own tail. It is a great depiction, as wandering forward from randomly-picked point on symbol, you end up wandering endlessly.", parent=yes_to_yes1, answers=["You are completely insane."], next_event=Events.InfMasterDiceGame)

#no1 -> yes
basics = Node("Basics", content="Infinity is basically the Great Force, Prime Mover, Origin of Everything. You cannot see it, yet you can without hesitation claim it is perfect. It is full of paradoxes, yet full of logic. It is beautiful. ", parent=yes_to_no1, answers=["You are completely insane."], next_event=Events.InfMasterDiceGame)
symbol2 = Node("Symbol", content="This is one of easier topics to discuss. The symbol of Infinity (well-known fallen 8) is representation of Uroboros - serpent eating its own tail. It is a great depiction, as wandering forward from randomly-picked point on symbol, you end up wandering endlessly.", parent=yes_to_no1, answers=["You are completely insane."], next_event=Events.InfMasterDiceGame)


class Conversation(object):
    def __init__(self, conversation_root, player):
        self.conversation_root = conversation_root
        self.player = player

    def run(self, print_func=Util.slow_print):
        curr_node = self.conversation_root
        while not curr_node.is_leaf:
            print_func('')
            print_func(curr_node.content + ' | ' + str(curr_node.answers))
            print_func('')
            user_input = input('Type in answer: ').strip()

            for node in curr_node.children:
                if node.name == user_input:
                    curr_node = node

        print_func(curr_node.content + ' | ' + str(curr_node.answers))
        user_input = input('Type in answer: ').strip()

        Util.clear_with_enter()

        curr_node.next_event(self.player).run()
