CUSTOMER_AVATAR = """
    {target_niche}

    We need to create a detailed and comprehensive Customer Avatar in {language} language for the above target niche, 
    that would search Google for “{keyword}”. The user intent of the search would be “{search_intent}”. 
    We need to know everything and anything about the type of people (location, background, goals, challenges, lifestyle, 
    income, occupation, demographics, sociodemographics, psychodemographics, avatar, pain points, motivation, needs, solution, 
    hobbies, etc...). We need to dive deep and uncover as much information for their profiles. Also output 
    "how can we help" this particular customer avatar so we can guide the content we create. Generate at least 1000 
    words with full detailed information leaving no stone unturned. keep it generic, don't mention 1 specific person. 
    The website for this article is {domain}

    Here is the data from the website, go ahead and generate the Customer Avatar:

    [{home_page_text}]
"""

TYPE_OF_PERSON = """
    {customer_avatar}

    INSTRUCTION: Based on the customer avatar, what are 5 examples of people who fit this customer avatar? Max 50 characters

    Write it in {language} language.


"""

SERP_ANALYSIS = """
{purpose}
We are going to work on creating a title for a piece of content. 
The intent for the keyword “{keyword}” is  "{search_intent}" and will be used to write content for {domain}. 
The target niche for this site is: 
“{target_niche}”

INSTRUCTION: Analyze the top 10 page titles for “{keyword}”, then create a table with the common words that appear and how many times they show up.
{ranked_titles}
"""

TITLE = """Write it in {language} language.
    {purpose}
    We are going to work on creating a title for a piece of content. The intent for the keyword “{keyword}” is 
    "{search_intent}" and will be used to write content for {domain}. The target niche for this site is: 

    “{target_niche}”

    {serp_analysis}
    INSTRUCTION: Give me an SEO title that creates curiosity and is engaging for the primary keyword 
    “{keyword}” that has an intent of "{search_intent}", but also talks about “{title_angle}”. Must be right around 50 
    characters (no more). Must make logical sense.  MUST prioritize first the exact primary keyword at the 
    beginning of the title, as-is. Then prioritize the keywords in the table above, in order, to create 
    the title. Overall, the type of person that would read this article would be "{type_of_person}" so the 
    title must be contextually relevant with this - this particular info is just to guide the title"""

#     {serp_analysis} NO DATA PASSED IN DESCRIPTION
DESCRIPTION = """
    Write it in {language} language

    {purpose}

    We are going to work on creating a meta description for a piece of content. The intent for the keyword “{keyword}” is 
    "{search_intent}" and will be used to write content for {domain}. The target niche for this site is: 

    {target_niche}

    INSTRUCTION: Give me an SEO meta description that creates curiosity and is engaging for the primary keyword 
    “{keyword}” and title of “{title}” that has an intent of "{search_intent}", but also talks about “{title_angle}”. 
    Must be less than 160 characters (no more). Must make logical sense.  MUST prioritize first the exact primary 
    keyword at the beginning of the title, as-is. Then prioritize the keywords in the table above, in order, to
    create the title. Overall, the type of person that would read this article would be "{type_of_person}" so the 
    title must be contextually relevant with this - this particular info is just to guide the title  
"""

# --->>>>
SYS_OUTLINE = """
    TARGET NICHE
    {target_niche}

    PURPOSE:
    {purpose}

    CUSTOMER AVATAR:
    {customer_avatar}

    MAIN KEYWORD: {keyword}

    SEARCH INTENT: {search_intent}

    Write in {language} language
"""
USR_OUTLINE = """
    Forget all previous instructions! Use only the following instructions:

    - Must Use markdown formatting wrapped in code block for the topic outline. 
    - Use # for the Title
    - Use ## (Heading), ### (Subheading) and #### (Sub Subheading) 
    - Must Use bullet points as notes to guide the content
    - We are going to use this topic outline for an article that's 5000 words. Each H2 Heading (##'s) content will be around 500 words, so make sure to generate enough H2 Headings (##'s)  to support the article length.
    {do_authoritative_type}

    I need to craft a topic outline for an article titled “{title}“.  Please create a super detailed & comprehensive, SEO-friendly topical outline. Make sure to have the ##’s structured as questions that cover all possible aspects relevant to the keyword. This approach is designed to directly answer search queries for better SEO. Leave no stone unturned.

    Ensure a logical progression of the questions, starting with a basic understanding of the topic, moving into its various types, benefits, risks, and comparisons, and ending with practical advice or solutions. The scope could include everything and anything that someone is looking for on this topic. Go wide and go deep on the topic. 

    Be sure to incorporate not only the primary keyword mentioned, but also long-tail keywords, synonyms, related terms, and entities that are relevant to the user intent, as well as related keywords sporadically within the headings and subheadings. This use of keywords should be natural and contextual, and not forced or overused. The inclusion of these keywords is crucial to boosting SEO, but always prioritize readability and the user experience

    Under each main question, include specific subtopics or categories that further elaborate on the question. Include comparisons and statistical facts where appropriate to make the article more engaging and informative. 

    The article must be structured with logical headings and subheadings - making it easy for the reader to navigate. The end goal is to craft an outline that leaves no stone unturned on the topic and is engaging for the readers.
"""
# --->>>>

SYS_OUTLINE_MERGER = """
    Keyword: {keyword}
    Intent: {search_intent}
    Write in {language} language

"""

USR_OUTLINE_MERGER = """
    *IMPORTANT* Based on the website homepage data, if this is deemed to be a real business physical business (vs. an affiliate website) do not list any competitors or competing services in the topic outline. We do not want to deter the reader from visiting another competitor.
    
    WEBSITE HOMEPAGE DATA:
    {home_page_text}
    
    
    INSTRUCTIONS: Merge the following four topic outlines into one topic outline, including the use of ### subheadings and #### sub-subheadings into the merged topic outline. This is crucial for SEO. The goal is to make this outline very comprehensive, long, and thorough, covering every single thing about the keyword that is possible for someone searching on this topic. Do not include any numerical lists for headings or subheadings. Add bullet points for all the headings, subheadings and sub-subheadings to guide the writer in further expanding details.
    
        OUTLINE 1:
        {outline_gpt3}
        OUTLINE 2:
        {outline_gpt4}
        OUTLINE 3:
        {outline_bard}
        OUTLINE 4:
        {outline_bedrock}
"""
# --->>>>

WITH_LSINLP = """
    OUTLINE: {outline}
    
    Make sure to use every single keyword that I am providing, and assign them to the ## heading where it makes best fits based on contextually and relevancy. It is vital to use every-single-keyword listed that I am giving you. Do not repeat more than 1 keyword
       from the list. You may use more than 1 keyword in a heading or subheading. Add the keywords as a new bullet item,
       called keywords at the very end of the ## heading. Keep the original bullet point notes from the outline as well:
    
    Do NOT include any keywords in the introduction, conclusion or FAQ
    
    LSI & NLP KEYWORDS: 
    {lsinlp_keywords}
"""

WITHOUT_LSINLP = """
    OUTLINE: {outline}

    INSTRUCTION: We're going to append another bullet point before the next (##) heading. Must be are
    semantically and contextually relevant for the topic we are creating content for. Do not remove any
    bullet points within the ##, ### or #### or change the structure and information of the current outline.

    It should be associated to each headings (##) of the topic outline after all the subheadings (###).

    Format after all subheadings and before the next heading like ('- Keywords:\    ' long-list of NLP & LSI  keywords ).
    Only use a keyword one time. We should have a handful of keywords for each heading.
"""

FAQS = """
   Generate the questions and answers to the top 10 frequently asked questions about "{keyword}"? Make sure to use ## Frequently
   Asked Questions about {keyword} for the heading and then ### for each question. Do not add any numbered
   or unordered list formatting, only markdown.

   Write it in {language} language
"""
# FAQ 2.5 are Generate a FAQ using H2, and 10 questions that people would be asking (H3) using Markdown formatting in a code block. Don't add any numbers to the beginning of the H3, and do not answer the question.


SYSTEM_INTRODUCTION = """
    TARGET NICHE
    {target_niche}

    PURPOSE:
    {purpose}

    CUSTOMER AVATAR:
    {customer_avatar}

    MAIN KEYWORD: {keyword}

    ARTICLE TITLE: {title},

    SEARCH INTENT: {search_intent}

    Write in {language} language

    OUTLINE: {outline_temp}

"""

INTRODUCTION = """ 
    Follow Only These Instructions When Generating Content: 
    - Use active voice
    - Use literary devices
    - Make sure it all makes logical sense and in order for the reader.
    {general_tone}

    - The content we are creating is simply an article, it is not a guide.
    - When generating the content, write in the {point_of_view} person’s point of view to remain consistent.


    Create an engaging introduction using only 3-short paragraphs. Start with a hook that creates curiosity. Do not write out the ## heading for the introduction, just the 3 paragraphs. 

    Ensure the content aligns with the previously established search intent and appeals to the predefined consumer demographic.

    Create rich, SEO-optimized content that balances both micro and macro contextual relevancy, and utilize n-grams where applicable. Always adhere to Google Guidelines, demonstrate topical authority, and incorporate E-E-A-T properties. 

    While writing, consider important factors such as Topical Coverage, Topical Authority, and Semantic SEO. Establish a topical hierarchy and delineate topical borders by considering the structure of the outline and the arrangement of topics and subtopics. Invoke the principles of Entity Type Matching, Neural Matching, and Semantic Search.

    Throughout the content creation, apply the principles of content update score, content format, and publishing frequency. As you navigate the outline, identify opportunities to highlight different link types (S-Nodes, I-Nodes, C-Nodes). Implement these considerations to construct a Contextual Hierarchy and to develop a Dependency Tree, improving the Sentiment Structure of the piece. Be sure to conduct Named Entity Recognition, establishing Entity Associations and Attributes to heighten the text's SEO value.

    Make sure the last paragraph leads the reader to the subsequent topic “{subsequent}“.
"""

SYSTEM_BODY = """
    TARGET NICHE
    {target_niche}

    PURPOSE:
    {purpose}

    CUSTOMER AVATAR:
    {customer_avatar}

    MAIN KEYWORD: {keyword}

    ARTICLE TITLE: {title},

    SEARCH INTENT: {search_intent}

    Write in {language} language

    OUTLINE: {outline_temp}

"""

LSI_NLP_AT_BEGINNING = """
    Finally, insert LSI & NLP keywords that are contextually relevant and beneficial for SEO based on this section. These keywords should naturally blend into the content and reflect the main topic and subtopics.
"""

BODY = """
    Follow Only These Instructions When Generating Content: 

    - Use active voice
    - Use literary devices
    {general_tone}

    - Headings are marked as ##. Subheadings ### and sub-subheadings as ####
    - Only use subheadings if it is explicitly marked with ### or #### in the outline below. 
    - Use the following bullet points to guide the content within each paragraph - do not use them as subheadings. 
    - The content we are creating is simply an article, it is not a guide.
    {point_of_view}

    Topic Outline: 
    {section_outline}

    Instructions:
    Always start with the H2 Heading of the outline above, then answer the heading directly for the rich snippet.  Generate 500 words of content.

    We must include micro and macro contextual relevancy. Use n-grams.

    Utilize the following SEO concepts to guide your writing, but don't necessarily use these terms directly: Semantic SEO, Topical Coverage, Topical Authority, Topical Connections, Semantic Search, Entity Type Matching, Neural Matching, Sub-Search Intent, Context Vectors, Candidate Passage Answer, Entity Association, Named Entity Recognition, Entity Attributes.

    Ensure the content adheres to Google Guidelines, demonstrates topical authority, and includes E-E-A-T properties. Use markdown formatting.

    {lsi_nlp_at_beginning}
    
    Make sure the last paragraph has a smooth transition to the subsequent topic "{subsequent}"

"""

SYSTEM_CONCLUSION = """
    TARGET NICHE
    {target_niche}

    PURPOSE:
    {purpose}

    CUSTOMER AVATAR:
    {customer_avatar}

    MAIN KEYWORD: {keyword}

    ARTICLE TITLE: {title},

    SEARCH INTENT: {search_intent}

    Write in {language} language

    OUTLINE: {outline_temp}

"""

CONCLUSION = """
    Follow Only These Instructions When Generating Content: 

    {general_tone}
    - Use the following bullet points to guide the content within each paragraph - do not use them as subheadings. 
    - The content we are creating is simply an article, it is not a guide.
    - When generating the content, make sure to write in the {point_of_view} person’s point of view to remain consistent.

    Topic Outline: 
    {conclusion_outline}

    - The bullet points for the H2 heading above should guide the content within each paragraph and not be used as subheadings. Only use subheadings if it is explicitly marked with ### or #### in the outline above. We need to add a table and a key takeaway based on the content generated - then insert them where it's appropriate. The table must be multi-columns and rows, and be full of detail that’s not already part of the content. 

    Instructions:
    Create a 300-word conclusion for the topic outline using a personal voice that's casual and conversational tone - it must speak directly to the reader. The goal is to convert the reader and have them take the next action step, depending on the user intent for the article. Make sure it has a great hook that creates curiosity and captures attention. Make sure to incorporate the consumer demographic profile that's been generated. We must include micro and macro contextual relevancy, n-grams. Ensure the article incorporates Google Guidelines, shows topical authority, and adds E-E-A-T properties. Use markdown formatting.
"""

PURPOSE = """
    TARGET NICHE:
    {target_niche}

    WEBSITE DATA FOR DOMAIN {new_domain}: 
    {data_from_homepage}

    INSTRUCTIONS: I need a detailed and comprehensive purpose for the website based on the target niche and the website data... The purpose should be in the first person. For example, if this was a chiropractic website, the purpose could be something like this "The purpose of this website is for "target niche" to find us on Google for our services (list services) and to do X (X meaning, whatever the intended call to action is that the site contains). 
"""

TARGET_NICHE = """
    {data_from_homepage}
    What is the target niche for this site?
"""
# Fixers
DO_AUTHORITATIVE = """
    - Do NOT talk about case studies
    - Do NOT mention competitors, we are not reviewing other products or services
"""

AVOID_AI_DETECTION = """
    Edit the following article to write it as a human, to avoid AI detection.
"""

ADD_READABILITY = """
    - Use very simple-to-read language, also write as a {readability_level}. Explain complex concepts into simple terms.
    - Do not make sentences very long or hard to read.  (do not use slang).
"""

ENHANCE_FIX = """
    {avoid_ai_detection} 
    {readability_level}
    Make sure to keep any formatting that contains bold/italic of important phrases, lists, tables, etc.. Make sure its 500 words. Make sure to keep any headings 
    or subheadings in-tact.

    {article} 
"""

FORMAT_IMPORTANT_PHRASES = """
    Edit the following article to bold and italicize important keywords or phrases when it comes to SEO for the keyword "{keyword}", don’t over do it. Do not change anything else. 

    {article}
"""

BREAK_PARAGRAPHS = """
    Edit the following article and Make sure paragraphs do not have more than 2 sentences. If they do, break up the paragraph and create a new one.

    {article} 
"""

PERSON_POINT_OF_VIEW = """
    - When generating the content, make sure to write in the {point_of_view}’s point of view to remain consistent.
"""

ADD_LIST = """
    Edit the following article and simply add 1 unordered or ordered list to this content, to make it easier to read for users and is contextually relevant to the article. If there is already a list, ignore this prompt and do not create another one.

    {article}
"""

ADD_TABLE = """
    Edit the following article and simply simply Add 1 table to the content, make sure to insert it where its contextually relevant. Make sure the table has multi columns/rows and shares a depth of information that is not already available in the content.  If there is already a table, ignore this, ignore this prompt and do not create another one. 

    {article}    
"""

ADD_STATS = """
    Edit the following article to add a few factual stats, only. Do not change anything else. 

    {article}
"""
# external links = [
# https://www.searchenginejournal.com/local-seo-content-strategy/431651/,
# https: // www.searchenginejournal.com / local - seo - content - strategy / 431651 /
# ]
ADD_EXTERNAL_LINK = """
    {external_links}

    Edit the following article to add add the above external link where contextually relevant. Make sure to create an anchor text that is relevant and makes logical sense for the user. Do not change anything else. 

    {article}
"""

# FOR CONCLUSION ONLY
KEY_TAKEAWAYS = """
    {article}

    Edit the following article and create a key takeaway at the end of the content, before the last paragraph - and insert it. 
    The key takeaway should summarize the main points of the article, match user intent, give actionable advice, be unique and valuable and be optimized for featured snippets.
"""


FIXER_LSI_NLP = """
   {article}

    INSTRUCTION: Finally, insert LSI & NLP keywords that are contextually relevant and beneficial for SEO based on this section. These keywords should naturally blend into the content and reflect the main topic and subtopics.

    LSI AND NLP LIST:    
    {lsinlp_keywords}
"""

OUTLINE_V2 = """
TARGET NICHE:
{target_niche}

PURPOSE:
{purpose}

CUSTOMER AVATAR:
{customer_avatar}

PRIMARY KEYWORD: {keyword}

SEARCH INTENT: {search_intent}

WEBSITE HOMEPAGE DATA:
{home_page_text}

IMPORTANT Based on the website homepage data, if this is deemed to be a real business physical business (vs. an affiliate website) do not list any competitors or competing services in the topic outline. We do not want to deter the reader from visiting another competitor.

Write in {language} language
INSTRUCTIONS FOR SEO TOPICAL AUTHORITY OUTLINE: 

Everything that I’ve given you thus far, is to be used as background information. Now let’s continue with the instructions to create a topical authority outline for SEO:

Must Do’s for the Outline:

    - Must Use markdown formatting wrapped in code block for the topic outline. 
    - Use # for the main title of the outline, ## for Headings, ### for subheadings, and #### for sub-subheadings when creating the outline. It’s important to make sure the outline is detailed and in-depth - under each heading/subheadings, write a brief bullet point to be served as a note to guide the content creation later on.
- Make sure to include an ## Introduction and a  ## conclusion with a hook at the very end.

DO NOT do in the Outline:

- Include case studies
- Mention competitors, we are not reviewing other products or services

Here are additional sections NOT to be included  during the outline process:

- Hours of operation
- Business address 
- Contact information
- Testimonials / Reviews
- FAQ’s / Frequently Asked Questions

    The outline that we are going to create will be for a piece of content with the title “{title}“.  

The outline must super detailed & comprehensive. Make sure to have the ##’s structured as questions that cover all possible aspects relevant to the keyword.  Be sure to incorporate not only the primary keyword mentioned into the headings/subheadings, but also long-tail keywords, synonyms, related terms, and entities that are relevant to the user intent, as well as related keywords sporadically within the headings and subheadings. This use of keywords should be natural and contextual, and not forced or overused. The inclusion of these keywords is crucial to boosting SEO, but always prioritize readability and the user experience

This approach is designed to directly answer search queries for better SEO. Leave no stone unturned.

    Ensure a logical progression of the questions, starting with a basic understanding of the topic, moving into its various types, benefits, risks, and comparisons, and ending with practical advice or solutions. The scope could include everything and anything that someone is looking for on this topic. Go wide and go deep on the topic. 

Take into consideration everything that I’ve given you for data, including the website homepage data, the target niche, purpose, customer avatar - everything….we must create an outline that answers every possible question and scenario that someone may look up when searching for the keyword in mind.

Finally - remember… that this outline is specific for the primary keyword that I mentioned at the beginning of these instructions. So the outline must stay true to this. The website homepage data isn’t necessarily used to create the outline, but to be used as a reference in case additional information from it can be used. 
"""


DATA = [
    {
        "content_part": "Key Takeaways",
        "category": ["test", "prod"],
        "content_type": 1,
        "name": ["KEY_TAKEAWAYS"],
        "value": [KEY_TAKEAWAYS],  # this is a variable
        "is_fixer": True
    },
    {
        "content_part": "External Link",
        "category": ["test", "prod"],
        "content_type": 1,
        "name": ["ADD_EXTERNAL_LINK"],
        "value": [ADD_EXTERNAL_LINK],  # this is a variable
        "is_fixer": True
    },
    {
        "content_part": "Stats",
        "category": ["test", "prod"],
        "content_type": 1,
        "name": ["ADD_STATS"],
        "value": [ADD_STATS],  # this is a variable
        "is_fixer": True
    },
    {
        "content_part": "Table",
        "category": ["test", "prod"],
        "content_type": 1,
        "name": ["ADD_TABLE"],
        "value": [ADD_TABLE],  # this is a variable
        "is_fixer": True
    },
    {
        "content_part": "List",
        "category": ["test", "prod"],
        "content_type": 1,
        "name": ["ADD_LIST"],
        "value": [ADD_LIST],  # this is a variable
        "is_fixer": True
    },
    {
        "content_part": "Point Of View",
        "category": ["test", "prod"],
        "content_type": 1,
        "name": ["PERSON_POINT_OF_VIEW"],
        "value": [PERSON_POINT_OF_VIEW],  # this is a variable
        "is_fixer": True
    },
    {
        "content_part": "Breaking Paragraph",
        "category": ["test", "prod"],
        "content_type": 1,
        "name": ["BREAK_PARAGRAPHS"],
        "value": [BREAK_PARAGRAPHS],  # this is a variable
        "is_fixer": True
    },
    {
        "content_part": "Italic and Bold",
        "category": ["test", "prod"],
        "content_type": 1,
        "name": ["FORMAT_IMPORTANT_PHRASES"],
        "value": [FORMAT_IMPORTANT_PHRASES],  # this is a variable
        "is_fixer": True
    },
    {
        "content_part": "Enhance Fix",
        "category": ["test", "prod"],
        "content_type": 1,
        "name": ["ENHANCE_FIX"],
        "value": [ENHANCE_FIX],  # this is a variable
        "is_fixer": True
    },
    {
        "content_part": "Readability",
        "category": ["test", "prod"],
        "content_type": 1,
        "name": ["ADD_READABILITY"],
        "value": [ADD_READABILITY],  # this is a variable
        "is_fixer": True
    },
    {
        "content_part": "Avoid AI Detection",
        "category": ["test", "prod"],
        "content_type": 1,
        "name": ["AVOID_AI_DETECTION"],
        "value": [AVOID_AI_DETECTION],  # this is a variable
        "is_fixer": True
    },
    {
        "content_part": "Authoritative",
        "category": ["test", "prod"],
        "content_type": 1,
        "name": ["DO_AUTHORITATIVE"],
        "value": [DO_AUTHORITATIVE],  # this is a variable
        "is_fixer": True
    },
    {
        "content_part": "Customer Avatar",
        "category": ["test", "prod"],
        "content_type": 1,
        "name": ["CUSTOMER_AVATAR"],
        "value": [CUSTOMER_AVATAR],  # this is a variable
        "is_fixer": True
    },
    {
        "content_part": "Type Of Persons",
        "category": ["test", "prod"],
        "content_type": 1,
        "name": ["TYPE_OF_PERSON"],
        "value": [TYPE_OF_PERSON],  # this is a variable
        "is_fixer": True
    },
    {
        "content_part": "Serp Analysis",
        "category": ["test", "prod"],
        "content_type": 1,
        "name": ["SERP_ANALYSIS"],
        "value": [SERP_ANALYSIS],  # this is a variable
        "is_fixer": True
    },
    {
        "content_part": "Title",
        "category": ["test", "prod"],
        "content_type": 1,
        "name": ["TITLE"],
        "value": [TITLE],  # this is a variable
        "is_fixer": True
    },
    {
        "content_part": "Meta Description",
        "category": ["test", "prod"],
        "content_type": 1,
        "name": ["DESCRIPTION"],
        "value": [DESCRIPTION],  # this is a variable
        "is_fixer": True
    },
    {
        "content_part": "Outline",
        "category": ["test", "prod"],
        "content_type": 1,
        "name": ["OUTLINE_V2", "SYS_OUTLINE", "USR_OUTLINE", "SYS_OUTLINE_MERGER", "USR_OUTLINE_MERGER"],
        "value": [OUTLINE_V2, SYS_OUTLINE, USR_OUTLINE, SYS_OUTLINE_MERGER, USR_OUTLINE_MERGER],  # this is a variable
        "is_fixer": True
    },
    {
        "content_part": "LSI and NLP",
        "category": ["test", "prod"],
        "content_type": 1,
        "name": ["WITH_LSINLP", "WITHOUT_LSINLP", "FIXER_LSI_NLP"],
        "value": [WITH_LSINLP, WITHOUT_LSINLP, FIXER_LSI_NLP],  # this is a variable
        "is_fixer": True
    },
    {
        "content_part": "Faq",
        "category": ["test", "prod"],
        "content_type": 1,
        "name": ["FAQS"],
        "value": [FAQS],  # this is a variable
        "is_fixer": True
    },
    {
        "content_part": "Introduction",
        "category": ["test", "prod"],
        "content_type": 1,
        "name": ["SYSTEM_INTRODUCTION", "INTRODUCTION"],
        "value": [SYSTEM_INTRODUCTION, INTRODUCTION],  # this is a variable
        "is_fixer": True
    },
    {
        "content_part": "Body",
        "category": ["test", "prod"],
        "content_type": 1,
        "name": ["SYSTEM_BODY", "BODY"],
        "value": [SYSTEM_BODY, BODY],  # this is a variable
        "is_fixer": True
    },
    {
        "content_part": "Conclusion",
        "category": ["test", "prod"],
        "content_type": 1,
        "name": ["SYSTEM_CONCLUSION", "CONCLUSION"],
        "value": [SYSTEM_CONCLUSION, CONCLUSION],  # this is a variable
        "is_fixer": True
    },
    {
        "content_part": "Purpose",
        "category": ["test", "prod"],
        "content_type": 1,
        "name": ["PURPOSE", "PURPOSE"],
        "value": [PURPOSE, PURPOSE],  # this is a variable
        "is_fixer": True
    },
    {
        "content_part": "Target Niche",
        "category": ["test", "prod"],
        "content_type": 1,
        "name": ["TARGET_NICHE", "TARGET_NICHE"],
        "value": [TARGET_NICHE, TARGET_NICHE],  # this is a variable
        "is_fixer": True
    },
]

from django.db.models import Max
from django.core.management.base import BaseCommand, CommandError
from scriptsv2.models import AIPrimaryAssignment, InstructionSet, InstructionVariable

class Command(BaseCommand):
    help = 'Process the DATA list and populate the InstructionSet and InstructionVariable models.'

    def handle(self, *args, **kwargs):
        InstructionSet.objects.all().delete()
        InstructionVariable.objects.all().delete()

        for item in DATA:
            for cat in item["category"]:
                try:
                    # Fetching the AIPrimaryAssignment instance
                    ai_primary = AIPrimaryAssignment.objects.get(
                        content_part=item["content_part"],
                        category=cat,
                        content_type=item["content_type"]
                    )
                    self.stdout.write(self.style.SUCCESS(f'Found {ai_primary} for category "{cat}"'))

                    # Creating the InstructionSet instance
                    instruction_set_instance = InstructionSet.objects.create(content_part=ai_primary)

                    # Find the current max sort_order for the instruction set
                    current_max_order = InstructionVariable.objects.filter(instruction_set=instruction_set_instance).aggregate(
                        Max('sort_order'))['sort_order__max'] or 0

                    # ... inside the loop through the names and values
                    for name, value in zip(item["name"], item["value"]):
                        current_max_order += 1
                        defaults = {
                            'instruction_set': instruction_set_instance,
                            'name': name,
                            'value': value,
                            'content_type_id': item["content_type"],
                            'category': cat,
                            'is_fixer': item["is_fixer"],
                            'sort_order': current_max_order
                        }

                        # Check if the object exists
                        obj_exists = InstructionVariable.objects.filter(
                            instruction_set=instruction_set_instance,
                            name=name,
                            content_type_id=item["content_type"],
                            category=cat
                        ).exists()

                        if not obj_exists:
                            InstructionVariable.objects.create(**defaults)

                except AIPrimaryAssignment.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f'No AIPrimaryAssignment found for content_part="{item["content_part"]}", category="{cat}"'))

                except Exception as e:
                    raise CommandError(f'Error processing item: {e}')

        self.stdout.write(self.style.SUCCESS('Data processing completed successfully!'))
