import logging
import boto3

from machine.plugins.decorators import process, route, respond_to, listen_to, require_any_role, on
from machine.plugins.base import MachineBasePlugin, Message
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)



class PipelinePlugin(MachineBasePlugin):
    """Pipeline Plugin"""

    def list_pipelines(self):
        client = boto3.client('codepipeline', region_name='us-gov-west-1')
        response = client.list_pipelines()
        return response['pipelines']

    @process("reaction_added")
    def match_reaction(self, event):
        logger.info(event)
        logger.info(self.bot_info)
        if not event['user'] == self.bot_info['user_id']:
            emoji = event['reaction']
            channel = event['item']['channel']
            ts = event['item']['ts']
            self.react(channel, ts, emoji)

    @route("/howdy")
    @route("/howdy/<name>")
    def my_exposed_function(self, name="World"):
        channel = self.find_channel_by_name('#test')
        self.say(channel, '{} is talking to me'.format(name))
        return {"howdy": name}

    @respond_to(r"^Me encanta")
    def encanta(self, msg):
        """I love you: express your love to the bot, it might reciprocate"""
        msg.react("heart")

    @listen_to(r"^users")
    def list_users(self, msg):
        """users: list all users in the Slack Workspace"""
        users = [u.name for u in self.users.values()]
        msg.say(f"{len(users)} Users: {users}")

    @listen_to(r"^pipelines$")
    def nag(self, msg):
        """pipelines: list the current CodePipelines"""
        pipelines = self.list_pipelines()
        for pipeline in pipelines:
            msg.say(pipeline['name'], in_thread=True)

    # @listen_to(r"^reply$")
    # def reply_me(self, msg: Message):
    #     """reply: the bot replies to you"""
    #     msg.reply("sure, I'll reply to you", icon_url="https://placekitten.com/200/200")

    # @listen_to(r"^reply ephemeral$")
    # def reply_me_ephemeral(self, msg: Message):
    #     """reply ephemeral: the bot replies to you and only you can see it"""
    #     msg.reply("sure, I'll reply to you in an ephemeral message", ephemeral=True)

    # @listen_to(r"^reply in thread$")
    # def reply_me_in_thread(self, msg: Message):
    #     """reply in thread: the bot replies to you in a thread"""
    #     msg.reply("sure, I'll reply to you in a thread", in_thread=True)

    # @listen_to(r"^dm reply$")
    # def dm(self, msg: Message):
    #     """dm reply: the bot replies to you in a DM"""
    #     msg.reply_dm("sure I'll reply to you in a DM")

    # @listen_to(r"^dm reply scheduled$")
    # def dm_scheduled(self, msg: Message):
    #     """dm reply scheduled: the bot replies to you at a later moment, in a DM"""
    #     msg.reply_dm("wait for it")
    #     dt = datetime.now() + timedelta(seconds=5)
    #     msg.reply_dm_scheduled(dt, "sure I'll reply to you in a DM after 5 seconds")

    # @listen_to(r"^admin")
    # @require_any_role(['admin'])
    # def admin(self, msg: Message):
    #     msg.say("You're an admin!")

    # @on("my-plugin-event")
    # def plugin_event_handle(self):
    #     channel = self.find_channel_by_name('#general')
    #     self.say(channel, "I'm listening to my-plugin-event")

    # @listen_to(r"^trigger my-plugin-event")
    # def trigger_plugin_event(self, msg: Message):
    #     self.emit("my-plugin-event")
