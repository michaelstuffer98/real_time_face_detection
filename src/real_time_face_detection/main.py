import argparse

from real_time_face_detection.create_user import setup as create_setup, main as create_main
from real_time_face_detection.face_training import setup as training_setup, main as training_main
from real_time_face_detection.real_time_recognition import setup as recognition_setup, main as recognition_main


def main():
    parser = argparse.ArgumentParser('real_time_face_detection', formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers()
    
    # Setup the parsers for the subcommands
    parser_create = subparsers.add_parser('create',
                                           help="""
Delegates to the create-user function
    Gives the possibility to manage user profiles and add more users
    This process includes feeding the pictures to the database""")

    parser_create = create_setup(parser_create)
    parser_create.set_defaults(func=create_main)

    parser_training = subparsers.add_parser('training',
                                             help="""
Delegates to the train-faces function
    Takes all the existing profiles and their photos and trains the model for later recognition""")

    parser_training = training_setup(parser_training)
    parser_training.set_defaults(func=training_main)
    
    parser_recognition = subparsers.add_parser('recognition',
                                                help="""
Delegates to the real-time-recognition function
    Starts the camera and hopefully recognizes you!""")

    parser_recognition = recognition_setup(parser_recognition)
    parser_recognition.set_defaults(func=recognition_main)
    
    parser.add_argument('--version', action='version', version='%(prog)s 0.1-Alpha')

    args = parser.parse_args()
    
    args.func(args)


if __name__ == '__main__':
    main()
