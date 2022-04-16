from configparser import ExtendedInterpolation
from email.message import _PayloadType
from burp import IBurpExtender
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator

from java.util import List, ArrayList

import random

class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory):
    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self._helpers = callbacks.getHelpers()

        callbacks.registerIntruderPayloadGeneratorFactory(self)

        return

    def getGeneratorName(self):
        return "BHP Payload Generator"

    def createNewInstance(self, attack):
        return BHPFuzzer(self, attack)


class BHPFuzzer(IIntruderPayloadGenerator):
    def __init__(self, extender, attack):
        self._extender = extender
        self._helpers = extender._helpers
        self._attack = attack
        self.max_payloads = 10
        self.num_iterations = 0

        return

    def hasMorePayloads(self):
        if self.num_iterations == self.max_payloads:
            return False
        else:
            return True

    def getNextPayload(self, current_payload):

        #converte em uma string
        payload = "".join(chr(x) for x in current_payload)

        #chama o nosso modificador simples para fazer fuzzing no POST
        payload = self.mutate_payload(payload)

        #incrementa o numero de tentativas de fuzzing
        self.num_iterations += 1

        return payload

    def reset(self):
        self.num_iterations = 0
        return 

    