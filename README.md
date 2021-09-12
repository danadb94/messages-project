For write message: /messages/
For get all messages for a specific user: user_messages/
For get all unread messages for a specific user: user_messages/unread_messages/
For read message: user_messages/ + message id
For delete message: /messages/ + message id

Assumptions:
- User can send a message to himself.
- User can send a message to multiple receivers.
- User can send a message with empty subject
- User can send a message with empty content
- User can read a message several times.
- Under unread_messages only messages users received will be displayed.
- User choose which message to read.

