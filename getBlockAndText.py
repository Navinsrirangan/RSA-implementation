import sys, math
 
def getBlocksFromText(message, blockSize):
     # Converts a string message to a list of block integers.
     blockInts = []
     for blockStart in range(0, len(message), blockSize):
         # Calculate the block integer for this block of text:
         blockInt = 0
         for i in range(blockStart, min(blockStart + blockSize,len(message))):
             blockInt += (ord(message[i])) * (128 **(i % blockSize))
         blockInts.append(blockInt)
     return blockInts


def getTextFromBlocks(blockInts, blockSize):
     # Converts a list of block integers to the original message string.
     # The original message length is needed to properly convert the last
     # block integer.
     message = []
     for blockInt in blockInts:
         blockMessage = []
         for i in range(blockSize-1,-1,-1):
             # Decode the message string for the 128 (or whatever
             # blockSize is set to) characters from this block integer:
             charIndex = blockInt//(128**i)
             blockInt = blockInt%(128**i)
             blockMessage.insert(0, chr(charIndex))
         message.extend(blockMessage)
     return "".join(message)
