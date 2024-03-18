from fastapi import FastAPI, HTTPException
from enum import Enum
from typing import Union
from pydantic import BaseModel


app=FastAPI( )

class Vote(BaseModel):
    answer:bool
    description:str
class Poll():
    name: str
    description: Union[str, None] = None
    aggreements:int = 0
    disagreements:int = 0
    votes:list[Vote] = []
class PollInfo(BaseModel):
    name:str
    description: Union[str, None] = None

polls:dict[str, Poll] = {}

@app.get("/poll/")
async def get_all_polls():
    return polls

@app.post("/poll/")
async def create_poll(info: PollInfo):
    if polls.get(info.name):
        # return {"message": "Poll with given name already exists - try different name"}
        raise HTTPException(status_code = 400, detail="Invalid action - poll with given name exists")
    else:
        new_poll:Poll = Poll()
        new_poll.name = info.name
        new_poll.description = info.description
        new_poll.aggreements = 0
        new_poll.disagreements = 0
        polls.setdefault(info.name, new_poll)
        return new_poll

@app.put("/poll/{poll_old_name}")
async def update_poll(poll_old_name:str, poll_info: PollInfo):
    old_poll = polls.pop(poll_old_name, None)
    if old_poll:
        if polls.get(poll_info.name) and poll_info.name != old_poll.name:
            polls.setdefault(old_poll.name, old_poll)
            # return {"message": "Poll with new name already exists - find other name"}
            raise HTTPException(status_code = 400, detail="Invalid action - poll with given name exists")
        old_poll.name = poll_info.name
        old_poll.description = poll_info.description
        polls.setdefault(poll_info.name, old_poll)
        return polls[poll_info.name]
    else:
        # return {"message":  "No poll found - You can just create new poll with such name :)"}
        raise HTTPException(status_code = 404, detail="Poll with given name does not exist")

@app.delete("/poll/{poll_name}")
async def delete_poll(poll_name:str):
    if polls.get(poll_name):
        out = polls.pop(poll_name)
        return {"message":"Deleted the poll", "poll":out}
    # return {"message": "No poll found"}
    raise HTTPException(status_code = 404, detail="Poll with given name does not exist")

@app.get("/poll/{poll_name}")
async def get_poll(poll_name:str):
    out = polls.get(poll_name)
    if out:
        return out
    # return {"message":"No poll found"}
    raise HTTPException(status_code = 404, detail="Poll with given name does not exist")


@app.post("/poll/{poll_name}/vote")
async def vote_in_poll(poll_name:str, vote: Vote):
    poll = polls.get(poll_name)
    if poll:
        poll.votes.append(vote)
        if vote.answer:
            poll.aggreements += 1 
        else:
            poll.disagreements += 1
        return poll
    # return {"message":"No poll with given name"}
    raise HTTPException(status_code = 404, detail="Poll with given name does not exist")


@app.get("/poll/{poll_name}/vote")
async def get_votes_in_poll(poll_name:str):
    poll = polls.get(poll_name)
    if poll:
        return poll.votes
    raise HTTPException(status_code = 404, detail="Poll with given name does not exist")

@app.get("/poll/{poll_name}/vote/{vote_id}")
async def get_vote_from_poll(poll_name:str, vote_id:int):
    poll = polls.get(poll_name)
    if poll:
        if 0 <= vote_id < len(poll.votes):
            return poll.votes[vote_id]
        raise HTTPException(status_code = 404, detail="Vote with given ID does not exist")
    raise HTTPException(status_code = 404, detail="Poll with given name does not exist")


@app.put("/poll/{poll_name}/vote/{vote_id}")
async def get_vote_from_poll(poll_name:str, vote_id:int, vote:Vote):
    poll = polls.get(poll_name)
    if poll:
        if 0 <= vote_id <= len(poll.votes):
            poll.votes[vote_id] = vote
            return poll.votes[vote_id]
        raise HTTPException(status_code = 404, detail="Vote with given ID does not exist")
    raise HTTPException(status_code = 404, detail="Poll with given name does not exist")


@app.delete("/poll/{poll_name}/vote/{vote_id}")
async def get_vote_from_poll(poll_name:str, vote_id:int):
    poll = polls.get(poll_name)
    if poll:
        if 0 <= vote_id <= len(poll.votes):
            del poll.votes[vote_id]
            return poll.votes[vote_id]
        raise HTTPException(status_code = 404, detail="Vote with given ID does not exist")
    raise HTTPException(status_code = 404, detail="Poll with given name does not exist")
