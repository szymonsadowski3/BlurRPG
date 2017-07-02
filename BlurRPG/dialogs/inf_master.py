from anytree import Node, RenderTree

yn = ["Yes", "No"]

root = Node("1", content="Hello Discrete Wanderer! Tell me... Have you ever wondered about notion of Infinity?", answers=yn)

yes1 = Node("Yes", content="Well... Obviously, I have also had my meditation in this topic. Do you want to hear my conclusions?", parent=root, answers=yn)
no1 = Node("No", content="Well... Maybe you want to educate a bit in this topic?", parent=root, answers=yn)

#yes1
yes_to_yes1 = Node("Yes", content="Excellent! Please choose one from these topics. I don't have time to explore them all", parent=yes1, answers=["Nature", "Origin", "Symbol"])
no_to_yes1 = Node("No", content="Well... Maybe you are not worthy to hear about this after all... You came such a long way just to experience failure! Well, you are only some pathetic, worthless worm in the face of Infinity. In the name of Infinity I sentence you to death!")

#no1
yes_to_no1 = Node("Yes", content="That is great, but considering you have not done any contemplation in this field I can only teach you some simpler things. Choose one from them", answer=["Basics", "Symbol"])
no_to_yes1 = Node("No", content="Just what I thought about you! You do not even express your desire to enchance knowledge in this most important topic of all possible! I don't know if you even deserve to die. Just go away, you little worm!")

#yes1 -> yes
nature = Node("Nature", content="So you want to learn more about nature of Infinity. This is very difficult to discuss. Some claim that Infinity exist only in ones' minds. This is pure heresy! The Infinity is real! It Reason-For-Everything, Prime Mover. We are all only helpless worms, who should bend knees in face of the Infinity and hope for mercy...", answers=["You are completely insane."])
origin = Node("Origin", content="")