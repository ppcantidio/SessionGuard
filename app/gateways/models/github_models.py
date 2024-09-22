from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class Plan(BaseModel):
    name: str
    space: int
    collaborators: int
    private_repos: int

class GitHubUser(BaseModel):
    login: str
    id: int
    node_id: str
    avatar_url: str
    gravatar_id: str
    url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    received_events_url: str
    type: str
    site_admin: bool
    name: Optional[str]
    company: Optional[str]
    blog: Optional[str]
    location: Optional[str]
    email: Optional[EmailStr]
    hireable: Optional[bool]
    bio: Optional[str]
    twitter_username: Optional[str]
    notification_email: Optional[EmailStr]
    public_repos: int
    public_gists: int
    followers: int
    following: int
    created_at: datetime
    updated_at: datetime
    private_gists: int
    total_private_repos: int
    owned_private_repos: int
    disk_usage: int
    collaborators: int
    two_factor_authentication: bool
    plan: Plan

