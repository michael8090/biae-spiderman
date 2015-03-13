# Introduction #

﻿看了下，目前大概需要8张表：
(EUser = Enterprise User)
//EUser
User
EUser\_Counters (趋势：粉丝数)
VUserTag

Friendship
Status
EUserStatus\_Counters (趋势：状态被转发、评论次数)

Comment (用于分析那些用户进行了评论)
Repost (用于分析那些用户进行了转发)

相关API:
users/show 用户profile (及粉丝数、关注数)
users/counts 用户的粉丝数、关注数
statuses/user\_timeline 企业用户的状态列表 (含转发、评论数)
friendships/followers 企业用户的粉丝列表
tags/tags\_batch 批量获取用户标签 (获得V们的标签)
comments/show 对某状态的评论列表
statuses/repost\_timeline 对某状态的转发列表
friendship/friends 用户关注的人的列表 (以便获取用户还关注了哪些V，对用户进行分类)


问题：
**是否需要保存企业用户profile？是保存在User里还是另设一张表？** 还需要什么修改？
**划分任务**



# Details #



Add your content here.  Format your content with:
  * Text in **bold** or _italic_
  * Headings, paragraphs, and lists
  * Automatic links to other wiki pages