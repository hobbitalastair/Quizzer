""" A quizzer/flashcard style Tkinter program in python

    Designed for my drivers licence practice ;)

    A quiz runs like so:

    While running:
    - Prompts for a quiz to run
    - Parses and builds a quiz object
    - While quizzing:
      - Gets a question from the quiz
      - Checks the answer
      - Responds

    Features to add:

    - Randomization of the order of multichoice questions
    - Psuedo randomization of questions
    - Images
    - Letting sets of possible answers being allocated seperatly from questions
    - Adding more question types
    - CLI argparsing
    - Framebuffer UI

    Author: Alastair Hughes
    Contact: <hobbitalastair at yandex dot com>

    Changelog:

    10-6-2014

    Started!

    11-6-2014

    Started on parsing quiz files

    12-6-2014

    Moved the main control and flow logic into a BaseQuiz object

    17-6-2014

    Moved to a state based system for the CLI UI to allow universal event based
    programming

    21-6-2014

    Adjusted so that the Tk UI works, and moved some of the UI specific stuff
    into properties

    8-9-2014

    Moved the tk quiz part to another file to allow avoiding tk

"""

VERSION=0.1

try:
    from tkquiz import TkQuiz
except ImportError:
    # Failed to import tk!
    # This is so that the program falls back to the CLI interface
    tkquiz = None


from basequiz import BaseQuiz, \
                     Quiz, \
                     Question, \
                     QuizException, \
                     get_input


class CLIQuiz(BaseQuiz):
    """ CLI test quizzer
    
        Features to add:

        - Tab completion
        - Pictures replaced with ascii art
        - Better multichoice:
          - Randomly order the possible answers
          - Replace the question id with A/B/...
    """

    
    # CLI control functions
               

    def run(self):
        """ Run the quizzer
        
            This involves getting the state and acting as required
        """

        while self.running:
            state = self.get_state()
            
            # Get the prompt for the current state
            if state == self.NEW_QUESTION:
                self.next_question()
            elif state == self.REVEALING:
                self.accept_answer()
                self.next_question()
            elif state == self.NEW_QUIZ:
                self.new_quiz()
            elif state == self.ANSWER:
                # Get user input and continue
                user_input = self.prompt("Answer")
                if user_input != None:
                    # Collect an answer
                    self.answer = user_input
            else:
                raise NotImplementedError(
                          "{} does not support a state of {}".format(self,
                                                                     state))


    def prompt(self, message):
        """ Return the value of the prompt """

        result = None # Result

        value = get_input(message + ": ") # Get input

        #TODO: Implement other commands (?)
        if value.lower() == "quit":
            # Quit quizzing
            self.quit()
        elif value.lower() == "help":
            # Get help
            print(self.quiz_help)
        elif value.lower() == "cancel":
            # Cancel!
            self.cancel_quiz()
        else:   # Return the user input
            result = value

        return result

    
    # UI properties
 

    @property
    def answer(self):
        """ Return the current answer """

        return self._answer


    @answer.setter
    def answer(self, value):
        """ Set the current answer to 'value' """

        self._answer = value


    # UI specific functions


    def load_quiz(self):
        """ Load a new quiz from the user """

        user_input = self.prompt("New quiz")

        if user_input != None:
            try:
                self.quiz = Quiz(user_input)
            except QuizException as error:
                print("Quiz '{}' not loaded due to {}!".format(
                                               user_input, error))
            else:
                print("Quiz {} loaded".format(user_input))
        else:
            return None


    def display_question(self):
        """ Display the question currently loaded """

        sort = self.question.sort

        if sort == 'prompt':
            print(self.question.question)
        elif sort == 'multichoice':
            print(self.question.question)
            pairs = ["{}: {}".format(choice, self.question.choices[choice])
                     for choice in self.question.choices]
            choices = "    \n".join(pairs)
            print(choices)
        else:
            raise ValueError("Question sort '{}' not recognized!".format(sort))


    def set_answer_response(self, response):
        """ Print out the response to the answer """
        print(response)


if __name__ == "__main__":

    #TODO: Fix this hack

    if tkquiz != None:
        print("Trying to create a tkinter quiz!")
        try:
            quiz_ui = TkQuiz()
        except tk._tkinter.TclError:
            print("No X detected; falling back to a CLI quiz!")
            quiz_ui = CLIQuiz()
    else:
        print("No tkinter installed; falling back to a CLI quiz!")
        quiz_ui = CLIQuiz()
    
    quiz_ui.run()

