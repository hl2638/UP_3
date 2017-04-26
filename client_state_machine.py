# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *

class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s

    def set_state(self, state):
        self.state = state
        
    def get_state(self):
        return self.state
    
    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me
        
    def connect_to(self, peer):
        msg = M_CONNECT + peer
        mysend(self.s, msg)
        response = myrecv(self.s)
        if response == (M_CONNECT+'ok'):
            self.peer = peer                #doubt: what if multi-member?
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response == (M_CONNECT + 'busy'):
            self.out_msg += 'User is busy. Please try again later\n'
        elif response == (M_CONNECT + 'hey you'):
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = M_DISCONNECT
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc(self, my_msg, peer_code, peer_msg):
        # message from user is in my_msg, if it has an argument (e.g. "p 3")
        # the the argument is in my_msg[1:]
        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:
                
                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE
                    
                elif my_msg == 'time':
                    mysend(self.s, M_TIME)
                    time_in = myrecv(self.s)
                    self.out_msg += "Time is: " + time_in
                            
                elif my_msg == 'who':
                    mysend(self.s, M_LIST)
                    user_list = myrecv(self.s)
                    self.out_msg += "Here are all the users in the system:\n" + user_list
                    #done
                    pass
                            
                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    #self.out_msg += "Pretending to connect"
                    if self.connect_to(peer):
                        self.state = S_CHATTING
                        self.out_msg += "Connect to %s. Chat away!" % (peer)        #might change this message
                    #done
                    pass
                        
                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, M_SEARCH + term)
                    search_result = myrecv(self.s)
                    self.out_msg += search_result.strip().[1:]
                    #done
                    pass
                        
                elif my_msg[0] == 'p':
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, M_POEM + poem_idx)
                    poem_in = myrecv(self.s)
                    self.out_msg += poem_in.strip()[1:]
                    #done
                    pass

                else:
                    self.out_msg += menu
                    
            if len(peer_msg) > 0:
                if peer_code == M_CONNECT:
                    peer = peer_msg
                    self.out_msg += "Request from %s\n" % (peer)
                    self.peer = peer
                    self.state = S_CHATTING        #doubt: what if multi-member?
                    self.out_msg += "You are connected with %s. Chat away!" % (peer)
                    #done
                    pass
                    
#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out
                mysend(self.s, M_EXCHANGE + "[" + self.me + "] " + my_msg)
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''
            
            if len(peer_msg) > 0:    # peer's stuff, coming in
                self.out_msg += peer_msg
                #done
                pass

            # I got bumped out
            if peer_code == M_DISCONNECT:
                self.state = S_LOGGEDIN
                self.disconnect()
                #done
                pass

            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu
#==============================================================================
# invalid state                       
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)
            
        return self.out_msg

"""
IMPORTANT/MUST-DO
What's your preference for the final project?
Do you prefer to work in a group of 2 or a group of 3?
A. a group of TWO
B. a group of THREE
C. no preference

Fill in your A/B/C below
My selection: A
"""