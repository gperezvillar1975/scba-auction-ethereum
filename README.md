# scba-auction-ethereum
Smart contract for implementing auctions on the blockchain


# Project architecture

┌──────────────────────┐                ┌─────────────────┐                  ┌──────────────┐
│                      │                │WebSocket Server │   Commands       │              │
│                      │ ─────────────► │                 ├────────────────► │              │
│    JavaScript        │                │Event Controller │                  │              │
│                      │                │                 │◄──────────────── │              │
│                      │                └─────────────────┘   Events         │   Contract   │
│    FrontEND          │                                                     │              │
│                      │                                                     │              │
│                      │                                                     │              │
│                      │                                                     └──────────────┘
│                      │                ┌─────────────────┐                         ▲
│                      │                │                 │                         │
│                      │ ◄───────────── │  REST API       │ ────────────────────────┘
│                      │                │                 │      Commands
└──────────────────────┘                └─────────────────┘


# Auction Lifecycle

# Contract external callable methods
