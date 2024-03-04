import autogen
from autogen import config_list_from_dotenv
from autogen import AssistantAgent, UserProxyAgent, GroupChatManager,GroupChat

#Config OPENAI_API_KEY form env file.
config_list = config_list_from_dotenv(
    dotenv_file_path='D:\Staging_Activity\.env',
    filter_dict={
        "model":{
            "gpt-3.5-turbo"
        }
    }
)
llm_config = {"config_list":config_list, "cache_seed": 42, "temperature":0.0}
#Create three agents: user_proxy, coder, product manager
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    llm_config=llm_config,
    system_message="A human admin who will give the idea and run the code provided by coder.",
    human_input_mode="ALWAYS",
    code_execution_config={"work_dir":"coding",
                           "use_docker" : False,
    },
)
coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config,
    code_execution_config ={"use_docker" : False},
)
product_manager=autogen.AssistantAgent(
    name="product_manager",
    system_message="You will help break down the initial idea into a well scope requirement for the coder; Do not involve in future conversation or error fixing",
    llm_config=llm_config,
    code_execution_config ={"use_docker" : False},
)

#Agent Group Chat
group_chat = autogen.GroupChat(agents=[user_proxy,coder,product_manager], messages=[])
manager = GroupChatManager(
    groupchat=group_chat,
    llm_config = llm_config,
    code_execution_config ={"use_docker" : False}
)

#initialize a task
user_proxy.initiate_chat(
    manager, message = "Write a code that can determine a numer is prime or not"
)