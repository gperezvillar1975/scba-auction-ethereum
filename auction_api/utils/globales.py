mongodb_server = ""
mongodb_port = ""
mongodb_user = ""
mongodb_pass = ""
mongodb_uri = ""
mongodb_db = ""
auction_schema = {
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
            },
            "minItems": 1,
            "uniqueItems": True,
        }  
    },
    "requirted" : ["code","auctionClass","guaranteeDeposit","startDate","endDate","auctionLots"]
    }
bidder_schema = {
    "type" : "object",
    "properties" : {
        "id_number" : {"type" : "string"},
        "name" : {"type" : "string"},
        "surname" : {"type" : "string"},
        "email" : {"type" : "string"},
        "username" : {"type" : "string"},
        "pass_sha256" : {"type" : "string"},
        "wallet_address" : {"type" : "string"},
        "wallet_pk" : {"type" : "string"},
        "status" : {"type" : "number"}
    },
    "requirted" : ["id_number","email","username"]
    }