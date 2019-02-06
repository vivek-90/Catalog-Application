from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Database_setup import Base, Category, Item, User

engine = create_engine('sqlite:///catalogwithusers1.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

User1 = User(name="Vivek", email="vivekravindran.90@gmail.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Item for cricket
category1 = Category(user_id=1, name="Cricket")
session.add(category1)
session.commit()

Item1 = Item(user_id=1, name="Bat", description="Made for Users training and playing regular Leather Ball cricket High Quality Kashmir Willow Bat for Regular Leather Ball cricket Training and Practice.", category=category1)
session.add(Item1)
session.commit()

Item2 = Item(user_id=1, name="Ball", description="Made for Users who want to play hard tennis ball cricket Bright hard ball ideal for practice under lights", category=category1)
session.add(Item2)
session.commit()

Item3 = Item(user_id=1, name="Pad", description="These are three wooden poles of height 28 inches. It has a conical bottom and a horizontal groove across the top end. There are three stumps at each end, with two bails sitting across the top of them and are equally spaced to cover a width of 9 inches.", category=category1)
session.add(Item3)
session.commit()

Item4 = Item(user_id=1, name="Gloves", description="Made for Beginners discovering leather ball cricket.Ergonomic, comfortable cricket gloves", category=category1)
session.add(Item4)
session.commit()

Item5 = Item(user_id=1, name="Stumps", description="Made for Professional and leisure cricket matches. Good quality yellow colored wicket for professional and leisure cricket matches.", category=category1)
session.add(Item5)
session.commit()


# Item for Football
category2 = Category(user_id=1, name="Football")
session.add(category2)
session.commit()


Item1 = Item(user_id=1, name="Mini GoalPost", description="Are you looking for a football goal for matches with friends? Our design teams created this small football goal that is perfect for football games including both children and adults.", category=category2)
session.add(Item1)
session.commit()

Item2 = Item(user_id=1, name="Football", description="Made for perfecting your football technique.Looking for a ball to get started on the pitch? We have created the First Kick football with a high quality bounce to make it ideal for learning to play.!!", category=category2)
session.add(Item2)
session.commit()

Item3 = Item(user_id=1, name="Football Boots", description="Made for expert football players, playing on grass pitches and wanting a lightweight boot for more speed on the pitch.Looking for a lightweight boot? Our design teams have developed the CLR 900 boot using an ultralight and supple microfibre material for increased propulsion and ball feel during play.", category=category2)
session.add(Item3)
session.commit()


# Item for Badminton
category3 = Category(user_id=1, name="Badminton")
session.add(category3)
session.commit()


Item1 = Item(user_id=1, name="Racket", description="This badminton racket is very versatile, offering ease of handling and comfort during play. It is perfect for improvers playing regularly at a club.", category=category3)
session.add(Item1)
session.commit()

Item2 = Item(user_id=1, name="shuttlecock", description="This single shuttle will provide you with stable trajectories thanks to its plastic skirt. A small touch of colour keeps the shuttle nicely visible while in play.", category=category3)
session.add(Item2)
session.commit()

Item3 = Item(user_id=1, name="Easy Net", description="This badminton net is very simple to set up and take down, making it perfect for easily enjoying badminton with your family or friends. You can play anywhere, at any time.", category=category3)
session.add(Item3)
session.commit()


# Item for Squash
category4 = Category(user_id=1, name="Squash")
session.add(category4)
session.commit()


Item1 = Item(user_id=1, name="Squash Racket", description="This squash racket is perfect for getting started with squash thanks to its durability, large head with comfortable strike zone, and its anti-vibration system built into the core of the racket.", category=category4)
session.add(Item1)
session.commit()

Item2 = Item(user_id=1, name="Squash Ball", description="This ball has a low bounce and slow speed, making it perfect for advanced players when training. This ball can also be used in matches in cool weather.", category=category4)
session.add(Item2)
session.commit()

Item3 = Item(user_id=1, name="Shoes", description="Made for beginner or occasional squash players.This entry-price shoe is perfect for getting into squash", category=category4)
session.add(Item3)
session.commit()

# Item for Squash
category5 = Category(user_id=1, name="Cycling")
session.add(category5)
session.commit()


Item1 = Item(user_id=1, name="Cycle", description="Do you want a bike that has it all and can be taken anywhere? The Tilt 120 can be easily stored in the boot of a car. With its 6 speeds and mudguard, you're all set for an adventure.", category=category5)
session.add(Item1)
session.commit()

Item2 = Item(user_id=1, name="Lock with Key", description="Minimum protection at a very affordable price. This coil lock is best used for protecting small bike accessories.", category=category5)
session.add(Item2)
session.commit()

Item3 = Item(user_id=1, name="Foot Pump", description="Foot pump with a dual head to make it compatible with all valves.", category=category5)
session.add(Item3)
session.commit()

print "added category items!"