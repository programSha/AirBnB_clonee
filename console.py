#!/usr/bin/python3

"""entry point of the HBNB command interpreter"""

import cmd
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage
import re
import shlex
import sys

implemented_classes = ["BaseModel", "User", "State",
                       "City", "Amenity", "Place", "Review"]
"""module level variable, holding the list of classes
that the user can create an instance of
"""


def handle_cmd_with_two_args(*tokens):
    """handle_cmd_with_two_args: checks the user input and
    prints the appropriate error messsage or perform the
    intended action

    Args:
        (tokens): list of arguments passed to the command

    Returns:
        (int): 0 if the command is complete
        (int): 1 if the command is incomplete or false

    """

    if not tokens:
        print("{}".format("** class name missing **"))
        return 1

    if tokens[0] not in implemented_classes:
        print("{}".format("** class doesn't exist **"))
        return 1

    if len(tokens) < 2:
        print("{}".format("** instance id missing **"))
        return 1

    return 0


class HBNBCommand(cmd.Cmd):
    """Defines the behavior and functionalities
    of the HBNB Consol

    """
    prompt: str = "(hbnb) "
    """str: prompt asking for the user to type a command"""

    message = "Welcome to hbnb console. Type 'help' for a list of commands."
    line = "\n============================================================"
    # intro: str = message + line
    # """str: airbnb console welcome message"""

    def do_quit(self, line):
        """quit: exits from the command interpreter"""
        sys.exit(0)

    def do_EOF(self, line):
        """EOF: exits from the command interpreter"""
        return True

    def emptyline(self):
        """emptyline: executes when the command is an empty
        line or white space (nothing is done)
        """
        return

    def do_create(self, line):
        """create: creates a new object  of the specified type
        and saves it to the file_storage

        Usage: create <class name>
        """
        if not line:
            print("{}".format("** class name missing **"))
            return

        funcs_dict = {"BaseModel": BaseModel, "User": User,
                      "State": State, "City": City, "Amenity": Amenity,
                      "Place": Place, "Review": Review}

        if line in funcs_dict:
            obj = funcs_dict[line]()
            obj.save()
            print("{}".format(obj.id))
            return

        print("{}".format("** class doesn't exist **"))

    def do_show(self, line):
        """show: prints the string representation of an
        instance based on the class name and the id

        Usage: show <class name> <id>
        """

        # split the command (line) using shell-like syntax
        tokens: list[str] = shlex.split(line)

        # do nothing else if the user input is incomplete or false
        if handle_cmd_with_two_args(*tokens):
            return

        key: str = "{}.{}".format(tokens[0], tokens[1])
        objects: dict = storage.all()

        if key in objects:
            print(objects[key])
            return

        print("{}".format("** no instance found **"))

    def do_destroy(self, line):
        """destroy: deletes an instance based on the class name
        and id, then saves the change into the file storage

        Usage: destroy <class name> <id>
        """

        # split the command (line) using shell-like syntax
        tokens: list[str] = shlex.split(line)

        # do nothing else if the user input is incomplete or false
        if handle_cmd_with_two_args(*tokens):
            return

        key: str = "{}.{}".format(tokens[0], tokens[1])
        objects: dict = storage.all()

        if key in objects:
            del objects[key]
            storage.save()
            return

        print("{}".format("** no instance found **"))

    def do_all(self, line):
        """all: prints all string representation of all instances
        based or not on the class name

        Usage1: all
        Usage2: all <class name>
        """
        str_rep_list: str = []
        objects: dict = storage.all()

        if not line:
            for key, obj in objects.items():
                str_rep_list.append(str(obj))
            print(str_rep_list)
        else:
            if line not in implemented_classes:
                print("{}".format("** class doesn't exist **"))
                return

            for key, obj in objects.items():
                if obj.__class__.__name__ == line:
                    str_rep_list.append(str(obj))
            print(str_rep_list)

    def do_update(self, line):
        """update: updates an instance based on the class name
        and id by adding or updating attribute and then saves
        the change into the file storage. If the attribute value
        is made of more than one word, it must be enclosed in
        quotation marks

        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """

        # split the command (line) using shell-like syntax
        tokens: list[str] = shlex.split(line)

        # do nothing else if the user input is incomplete or false
        if handle_cmd_with_two_args(*tokens[0:2]):
            return

        key: str = "{}.{}".format(tokens[0], tokens[1])
        objects: dict = storage.all()

        if key not in objects:
            print("{}".format("** no instance found **"))
            return

        if len(tokens) < 3:
            print("{}".format("** attribute name missing **"))
            return

        if len(tokens) < 4:
            print("{}".format("** value missing **"))
            return

        attr_name, attr_value = tokens[2:4]
        try:
            attr_value = json.loads(attr_value)
        except Exception:
            pass

        # if hasattr(objects[key], attr_name):
        setattr(objects[key], attr_name, attr_value)
        objects[key].save()

    def default(self, line):
        """default: runs when the command is unknown. Will be used here
        to check if the command is using the new syntax or not and do
        what should be done according to the result

        syntax: <class_name>.method()
        """
        error_message: str = "*** Unknown syntax: {}".format(line)

        tokens = line.strip()
        tokens = tokens.split(".")

        # If we don't have exactly two tokens, the command is wrong
        if len(tokens) != 2:
            print(error_message)
            return

        # Get's the class name
        class_name = tokens[0]

        # Get's the method to call and eventually the arguments
        method = tokens[1]

        if class_name not in implemented_classes:
            print("{}".format("** class doesn't exist **"))
            return

        if method == "all()":
            self.class_all(class_name)
            return
        if method == "count()":
            self.class_count(class_name)
            return

        # Get's the opcode and the arguments in different variables
        opcode, rest = method.split("(")
        if rest:
            rest = rest[:-1]

        if not rest and (opcode == "show" or opcode == "destroy"):
            print("{}".format("** instance id missing **"))
            return

        if opcode == "show" or opcode == "destroy":
            rest = self.clean_str(rest)

        if opcode == "show":
            self.class_show(class_name, rest)
            return

        if opcode == "destroy":
            self.class_destroy(class_name, rest)
            return

        if opcode == "update":
            id_match = re.search(r'"[\w\-]+"', rest)
            if id_match is None:
                print("{}".format("** instance id missing **"))
                return
            else:
                id_match = id_match.group(0)

            dict_match = re.search(r'{.+}', rest)

            if dict_match is not None:
                # Replace any <'> by <"> to avoid exeption raising
                dict_match = dict_match.group(0).replace("'", "\"")
                try:
                    dict_match = json.loads(dict_match)
                except Exception:
                    print(error_message)
                    return
                self.class_update_kwargs(
                    class_name, self.clean_str(id_match), **dict_match)
                return

            attr_and_value = rest.split(", ")

            if len(attr_and_value) < 2:
                print("{}".format("** attribute name missing **"))
                return
            if len(attr_and_value) < 3:
                print("{}".format("** value missing **"))
                return

            attr, value = attr_and_value[1:3]
            self.class_update_arg(class_name, self.clean_str(id_match),
                                  self.clean_str(attr), self.clean_str(value))
        else:
            print(error_message)

    def class_all(self, class_name):
        """class_all: prints the string representation of all
        instances of a class

        usage: <class name>.all()
        """
        str_rep_list: str = []
        objects: dict = storage.all()

        for key, obj in objects.items():
            if obj.__class__.__name__ == class_name:
                str_rep_list.append(str(obj))
        print(str_rep_list)

    def class_count(self, class_name):
        """class_count: prints the number of instances of a class

        usage: <class name>.count()
        """
        objects: dict = storage.all()
        class_count = 0

        for key, obj in objects.items():
            if obj.__class__.__name__ == class_name:
                class_count += 1
        print(class_count)

    def class_show(self, class_name, obj_id):
        """class_show: prints the string representation an object
        based on his class name and id, or an error message

        usage: <class name>.show(<id>)
        """
        key: str = "{}.{}".format(class_name, obj_id)
        objects: dict = storage.all()

        if key in objects:
            print(objects[key])
            return

        print("{}".format("** no instance found **"))

    def class_destroy(self, class_name, obj_id):
        """class_destroy: deletes an object
        based on his class name and id, or an error message

        usage: <class name>.destroy(<id>)
        """
        key: str = class_name + "." + obj_id
        objects: dict = storage.all()

        if key in objects:
            del objects[key]
            storage.save()
            return

        print("{}".format("** no instance found **"))

    def class_update_arg(self, class_name, obj_id, attr, value):
        """class_update_arg: update the attribute of an object
        based on the class_name and id
        """
        key: str = class_name + "." + obj_id
        objects: dict = storage.all()

        if key in objects:
            # if hasattr(objects[key], attr):
            setattr(objects[key], attr, value)
            objects[key].save()
            return

        print("{}".format("** no instance found **"))

    def class_update_kwargs(self, class_name, obj_id, **dct):
        """class_update_kwargs: update the attribute of an object
        based on the class_name and id using a dict
        """
        key: str = class_name + "." + obj_id
        objects: dict = storage.all()

        if key in objects:
            for attr, value in dct.items():
                # if hasattr(objects[key], attr):
                setattr(objects[key], attr, value)
                objects[key].save()
            return

        print("{}".format("** no instance found **"))

    def clean_str(self, string):
        """clean_str: cleans a string by removing the a paire of
        single quote or double quote
        """
        if len(string) > 3:
            if string[0] == "\"" or string[0] == "\'":
                string = string[1:]
            if string[-1] == "\"" or string[-1] == "\'":
                string = string[:-1]
        return string


if __name__ == '__main__':
    HBNBCommand().cmdloop()
