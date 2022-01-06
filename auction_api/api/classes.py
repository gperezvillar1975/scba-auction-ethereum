class AuctionLot:
    id = ""
    startDate = 0
    endDate = 0
    baseValue = 0
    description = ""

class Auction:
    code = ""
    auctionClass = 0
    auctionStatus = 0
    guaranteeDeposit = 0
    startDate = 0
    endDate = 0
    __auctionLots = []
    __auction_schema = {
        "type" : "object",
        "properties" : {
            "code" : {"type" : "string"},
            "auctionClass" : {"type" : "number"},
            "auctionStatus" : {"type" : "number"},
            "guaranteeDeposit" : {"type" : "number"},
            "startDate" : {"type" : "number"},
            "endDate" : {"type" : "number"},
            "auctionLots" : {
                "type" : "array",
                "items" : {
                    "type" : "object",
                    "properties" : {
                        "description" : {"type" : "string"},
                        "baseValue" : {"type" : "number"}
                    },
                    "requirted" : ["baseValue","description"]
                }
            }
        },
        "requirted" : ["code","auctionClass","guaranteeDeposit","startDate","endDate","auctionLots"]
    }

    def addLot(self, description,baseValue):
        tmpLot = AuctionLot
        tmpLot.id = len(self.__auctionLots) + 1
        tmpLot.startDate = self.startDate
        tmpLot.endDate = self.endDate
        tmpLot.baseValue = baseValue
        tmpLot.description = description

        self.__auctionLots.append(tmpLot)

    def getLot(self, lotId):
        return self.__auctionLots[lotId-1]

    def getLotCount(self):
        return len(self.__auctionLots)

    def validateJSON(jsondata):
        pass
    def fromJSON(jsondata):
        pass
    def toJSON(jsondata):
        pass

