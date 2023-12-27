    class CustomClient(discord.Client):
        async def on_ready(self) -> None:
            try:
                logger.info(f"{self.user} has connected to Discord!")
                channel = client.get_channel(channel_id)
                # only work for text channels for now
                if not isinstance(channel, discord.TextChannel):
                    raise ValueError(
                        f"Channel {channel_id} is not a text channel. "
                        "Only text channels are supported for now."
                    )
                # thread_dict maps thread_id to thread
                thread_dict = {}
                for thread in channel.threads:
                    thread_dict[thread.id] = thread
                async for msg in channel.history(
                    limit=limit, oldest_first=oldest_first
                ):
                    messages.append(msg)
                    if msg.id in thread_dict:
                        thread = thread_dict[msg.id]
                        async for thread_msg in thread.history(
                            limit=limit, oldest_first=oldest_first
                        ):
                            messages.append(thread_msg)
            except Exception as e:
                logger.error("Encountered error: " + str(e))
            finally:
                await self.close()
