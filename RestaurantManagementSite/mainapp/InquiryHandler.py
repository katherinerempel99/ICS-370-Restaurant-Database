class InquiryHandler:
    def __init__(self):
        self.__queue = []   #holds newly created inquiries that have not been adapted into accepted events
        self.__inquiryKeeper = {}   # dict of inquiry info and callbacks

    def addInquiry(self,inquiryID):
        self.__queue.append(inquiryID) # inquiry is added to end of queue

    def getInquiryData(self,inquiryID): # retrieve all inputted data from inquiry from sql table
        self.__inquiryKeeper 
        pass

    def manageInquiry(self):
        # when User interacts with queue, the top inquiry is popped off and sent to a form(?) to be edited
        # if accepted and adapted into Event, remove from Inquiry table
        # if user cancels, inquiry is added to end of queue
        # if user rejects, inquiry is deleted from Inquiry table 
        pass