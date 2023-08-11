#
# We prompt the user to give a phrase and try to create pql from it
# using Microsoft Azure OpenAI.  We also feed the generated pql back to the model
# and ask it to explain the pql in plain English
#
# The model is trained using 50 examples prepended before each prompt
#
import os
import openai
openai.api_type = "azure"
openai.api_base = "https://southcentralus.api.cognitive.microsoft.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = <OPENAI_API_KEY>
#
# Our 50-shot training examples
#
promptStr = "\n\n# Native language\nPeople from Nevada\n# PQL\nhomeAddress.state.equals(\"NV\", false)\n###\n" \
          "# Native language\nPeople from Wisconsin\n# PQL\n\n\nhomeAddress.state.equals(\"WI\", false)\n###" \
          "\n\nNative language\npeople who were born before 2009\n# PQL\nperson.birthYear < 2009\n###\n" \
          "\n\nNative language\npeople who were born before 2009\n# PQL\nperson.birthDate.getYear() < 2009\n###\n" \
          "\n\nNative language\npeople were born this month\n# PQL\nperson.birthDate.getMonth() = today.getMonth()\n###\n" \
          "\n\nNative language\npeople who were born before 3/21/1979\n# PQL\nperson.birthDate occurs before date(1979, 3, 21)\n###\n" \
          "\n\nNative language\npeople who were born after 7/27/1962\n# PQL\nperson.birthDate occurs after date(1962, 7, 27)\n###\n" \
          "\n\nNative language\npeople who were born at least 30 years before today\n# PQL\nperson.birthDate occurs >= 30 years before today\n###\n" \
          "\n\nNative language\npeople who were born more than 18 years ago\n# PQL\nperson.birthDate occurs > 18 years before today\n###\n" \
          "\n\nNative language\npeople who were are at least 18 years old\n# PQL\nperson.birthDate occurs >= 18 years before today\n###\n" \
          "\n\nNative language\npeople who were born less than 50 years ago\n# PQL\nperson.birthDate occurs <= 50 years before today\n###\n" \
          "\n\nNative language\npeople who are less than 65 years old\n# PQL\nperson.birthDate occurs < 65 years before today\n###\n" \
          "\n\nNative language\npeople whos profile has a birth date\n# PQL\nperson.birthDate.isNotNull()\n###\n" \
          "\n\nNative language\nprofiles that have a person's birth year\n# PQL\nperson.birthYear.isNotNull()\n###\n" \
          "\n\nNative language\npeople who's country code is \"US\"\n# PQL\nhomeAddress.countryCode.equals(\"US\", false)\n###\n" \
          "\n\nNative language\nmen\n# PQL\nperson.gender = \"male\"\n###\n" \
          "\\n\nNative language\nwomen\n# PQL\nperson.gender = \"female\"\n###\n" \
          "\n\nNative language\nmen or women\n# PQL\nperson.gender in [\"male\", \"female\"]\n###\n" \
          "\n\nNative language\npeople who live in Caifornia\n# PQL\nhomeAddress.state.equals(\"CA\", true)\n###\n" \
          "\n\nNative language\npeople who's home state is CA\n# PQL\nhomeAddress.state.equals(\"CA\", true)\n###\n" \
          "\n\nNative language\npeople who live in the US state of New York\n# PQL\nhomeAddress.state.equals(\"NY\", false)\n###\n" \
          "\n\nNative language\npeople who's home state is \"TN\\n# PQL\nhomeAddress.state.equals(\"TN\", false)\n###\n" \
          "\n\nNative language\npeople who live in Great Britan\n# PQL\nhomeAddress.countryCode.equals(\"GB\", false)}\n###\n" \
          "\n\nNative language\npeople who live in the US states of California or Virginia\n# PQL\nstringCompare(\"equals\", homeAddress.state, [\"CA\", \"VA\"], false)\n###\n" \
          "\n\nNative language\npeople who live in Miami\n# PQL\nhomeAddress.city.equals(\"miami\", false)\n###\n" \
          "\n\nNative language\npeople who live in Iowa, Minnesota, North Dakota, Nebraska, South Dakota, or Wisconsin\n# PQL\nstringCompare(\"equals\", homeAddress.state, [\"IA\", \"MN\", \"ND\", \"NE\", \"SD\", \"WI\"], false)\n###\n" \
          "\n\nNative language\npeople who are in segment \"segId1\"\n# PQL\ninSegment(\"segId1\")\n###\n" \
          "\n\nNative language\npeople who are in segment \"segId2\" or segment \"segId3\"\n# PQL\ninSegment(\"segId2\") or inSegment(\"segId3\")\n###\n" \
          "\n\nNative language\npeople who are in segment \"segId4\" and segment \"segId5\"\n# PQL\ninSegment(\"segId4\") and inSegment(\"segId5\")\n###\n" \
          "\n\nNative language\npeople who are in segment \"segId6\" but not in segment \"segId7\"\n# PQL\ninSegment(\"segId6\") and not(inSegment(\"segId7\")\n###\n" \
          "\n\nNative language\npeople who have opted out of receiving email\n# PQL\noptInOut._channels.email = \"out\"\n###\n" \
          "\n\nNative language\npeople who have opted out of receiving marketing email\n# PQL\nconsents.marketing.email.val in [\"dn\", \"n\"]\n###\n" \
          "\n\nNative language\npeople who have opted in to receiving marketing email\n# PQL\noptInOut._channels.email = \"in\"\n###\n" \
          "\n\nNative language\npeople who's email address is \"s1@domain1.com\"\n# PQL\npersonalEmail.address.equals(\"s1@domain1.com\", false)\n###\n" \
          "\n\nNative language\npeople who's personal email address is \"s1@domain1.com\"\n# PQL\npersonalEmail.address.equals(\"s1@domain1.com\", false)\n###\n" \
          "\n\nNative language\npeople who's personal email address contains \"a\"\n# PQL\npersonalEmail.address.contains(\"a\", false)\n###\n" \
          "\n\nNative language\npeople who's profile has a personal email address\n# PQL\npersonalEmail.address.isNotNull()\n###\n" \
          "\n\nNative language\npeople who's profile does not conain a personal email address\n# PQL\npersonalEmail.address.isNull()\n###\n" \
          "\n\nNative language\npeople without a personal email address\n# PQL\npersonalEmail.address.isNull()\n###\n" \
          "\n\nNative language\npeople who's last name is \"s2\"\n# PQL\nperson.name.lastName.equals(\"s2\", false)\n###\n" \
          "\n\nNative language\npeople who work in California\n# PQL\nworkAddress.state.equals(\"ca\", false)\n###\n" \
          "\n\nNative language\npeople who are members of the customer journey audience \"s3\"\n# PQL\nsegmentMembership.get(\"CJAAudiences\").get(\"s3\").status in [\"realized\", \"existing\"]\n###\n" \
          "\n\nNative language\npeople who subscribe to the email marketing topic \"s4\"\n# PQL\nconsents.marketing.email.subscriptions.get(\"s4\").val = \"y\\n###\n" \
          "\n\nNative language\npeople who subscribe to the email marketing lis \"s99\"\n# PQL\nconsents.marketing.email.subscriptions.get(\"s99\").val = \"y\\n###\n" \
          "\n\nNative language\npeople who were born between 2/4/1974 and 9/17/2019\n# PQL\nperson.birthDate occurs between date(1974, 2, 4) and date(2019, 9, 17)\n###\n" \
          "\n\nNative language\npeople whose loyalty points are between 1000 and 3000\n# PQL\nloyalty.points > 1000.0 and loyalty.points < 3000.0\n###\n" \
          "\n\nNative language\npeople whose loyalty points are between 1000 and 3000, inclusive\n# PQL\nloyalty.points >= 1000.0 and loyalty.points <= 3000.0\n###\n" \
          "\n\nNative language\npeople whose loyalty status equals \"Active\"\n# PQL\nloyalty.status.equals(\"Active\", true)}\n###\n" \
          "\n\nNative language\npeople who are members of audience manager segment \"aam1\"\n# PQL\nsegmentMembership.get(\"AAMSegments\").get(\"aam1\").status in [\"realized\", \"existing\"]\n###\n" \
          "\n\nNative language\npeople who have joined the loyalty program\n# PQL\nloyalty.joinDate.isNotNull()\n###\n" \
          "\n\nNative language\npeople who have subscribed to the loyalty program\n# PQL\nloyalty.joinDate.isNotNull()\n###\n"


def compare_keys_values(dic, promptStr):
  for key, value in dic.items():
    response = getResponse(key, promptStr)
    print(value + " : " + response['choices'][0]['text'])
    if value.strip() != response['choices'][0]['text'].strip():
        print("failed")
        return False
    else:
        print("passed")
  return True


def generateCompletePrompt(prompt, promptStr):
    complete_prompt = promptStr + "# Native language\n" + prompt + "\n# PQL\n"
    return complete_prompt


def getResponse(prompt, promptStr):
    complete_prompt = generateCompletePrompt(prompt, promptStr)
    response = openai.Completion.create(
        engine="first_deploy_gpt_35_turbo_0301",
        #engine="curie-pql-training1",
        prompt=complete_prompt,
        temperature=0,
        max_tokens=1000,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["###"])
    return response


# prompts which return consistent results
test_dict_good = {'men': 'person.gender = \"male\"',
             'People from WA': 'homeAddress.state.equals(\"WA\", false)',
             'people who are in segment \"blah\"': 'inSegment(\"blah\")',
             'people who\'s last name is \"Grady\"': 'person.name.lastName.equals(\"Grady\", false)',
             'people who work in Arizona': 'workAddress.state.equals(\"AZ\", false)',
             'people who live in Washington': 'homeAddress.state.equals(\"WA\", false)',
             'people who have not joined the loyalty program': 'loyalty.joinDate.isNull()',
             'people who have joined the loyalty program and have an email address': 'loyalty.joinDate.isNotNull() and personalEmail.address.isNotNull()',
            'people who have joined the loyalty program, don\'t have an email address and have loyalty points greater than 3000': 'loyalty.joinDate.isNotNull() and personalEmail.address.isNull() and loyalty.points > 3000.0'
             }

# prompt which return different results
test_dict_neg = {'people who live in California, Nevada, Washington or Arizona': 'homeAddress.state in [\"CA\", \"NV\", \"WA\", \"AZ\"]',
             'people who were born less than 25 years ago': 'person.birthDate occurs <= 25 years before today'}

# current test dictionary
test_dict = {
             'people who have joined the loyalty program, don\'t have an email address and have loyalty points greater than 3000': 'loyalty.joinDate.isNotNull() and personalEmail.address.isNull() and loyalty.points > 3000.0'
             }

user_input = input("Describe your audience: ")
responseStr = getResponse(user_input, promptStr)
responseStrText = responseStr['choices'][0]['text']
print("\n==== Here is your PQL ===\n")
print(responseStrText)

print("\n==== Let me interpret the PQL I just gave you back into natural language ===\n")

# Start reverse process
#promptStr = "You are an AI assistant that helps people find information.You are an assistant that help intepret Adobe Profile Query Language (PQL) phrases into natural language."
#responseStr = getResponse(responseStr['choices'][0]['text'], promptStr)


returnResponse = openai.ChatCompletion.create(
  engine="first_deploy_gpt_35_turbo_0301",
  messages = [{"role":"system","content":"You are an AI assistant that helps people find information."},
              {"role":"user","content":"homeAddress.state in [\"CA\", \"ID\", \"WA\",\"AZ\"] and person.gender = \"male\" and loyalty.joinDate.isNotNull() and consents.marketing.email.val = \"y\" and person.birthDate occurs <= 20 years before today"},
              {"role":"assistant","content":"This query is checking for individuals who meet the following criteria:\n- They live in California, Idaho, Washington, or Arizona.\n- They identify as male.\n- They have joined a loyalty program and provided their birthdate.\n- They have given consent to receive marketing emails.\n- Their birthdate indicates that they are 20 years old or younger. \n\nIn summary, this query is looking for young male loyalty program members who have given consent to receive marketing emails and live in certain states."},
              {"role":"user","content":responseStrText}],
  temperature=0.7,
  max_tokens=800,
  top_p=0.95,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None)

print(str(returnResponse['choices'][0]['message']['content']))

print("=========================")





