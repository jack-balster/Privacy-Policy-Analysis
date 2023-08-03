# app.py
from flask import Flask, render_template, request
import openai
import os

# Create a Flask app instance
app = Flask(__name__)

# Set the OpenAI API key
openai.api_key = "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"

# Define a route for the index page that handles GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def index():
    # Check if the request is a POST request
    if request.method == 'POST':
        # Retrieve the user's input from the form field named 'privacy_agreement'
        privacy_agreement = request.form['privacy_agreement']
        if privacy_agreement:
            # Call the function to summarize the privacy agreement using ChatGPT
            summary = summarize_privacy_agreement(privacy_agreement)
        else:
            # Default message 
            summary = "Please enter a privacy agreement in the input box above"
            
        # Render the 'index.html' template and pass the summary to display on the page
        return render_template('index.html', summary=summary)
    # For GET requests or when the form is not submitted, render the 'index.html' template with an empty summary
    return render_template('index.html', summary='')

# Function to summarize text 
def summarize_privacy_agreement(text):
    # Check if the text exceeds the maximum token limit
    if len(text.split()) > 3500:
        # If it exceeds the limit, split the text into smaller segments
        segments = []
        current_segment = ""
        for word in text.split():
            if len(current_segment) + len(word) + 1 < 3500:  # Add 1 for space
                current_segment += " " + word
            else:
                segments.append(current_segment.strip())
                current_segment = word
        if current_segment:
            segments.append(current_segment.strip())

        # Summarize each segment separately using ChatGPT model
        summaries = []
        for segment in segments:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Please summarize the following and include a list of all the things a user gives the company access to: "},
                    {"role": "user", "content": segment},
                ],
                max_tokens=500 
            )
            summary = response.choices[0].message["content"].strip()
            summaries.append(summary)

        # Combine the summaries from all segments
        final_summary = " ".join(summaries)

        # Summarize the segments for the final summary
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Please summarize the following (be sure to still include the list of all the things the company has access to): "},
                {"role": "user", "content": final_summary},
            ],
            max_tokens=450 
        )
        final_summary = response.choices[0].message["content"].strip()

    else:
        # If the text doesn't exceed the token limit, summarize it directly
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Please summarize the following:"},
                {"role": "user", "content": text},
            ],
            max_tokens=400 
        )
        final_summary = response.choices[0].message["content"].strip()

    return final_summary


# Define route to get the summary for a specific preloaded company
@app.route('/get_summary/<company>', methods=['GET'])
def get_summary_by_company(company):
    summary_text = {
        'meta': 'Meta\'s data policy states that the company collects and processes user data to support its various products, including Facebook, Instagram, and Messenger. The types of information collected depend on how users use the products, and some examples include user-provided content, networks and connections, usage data, information about transactions, and information provided by others. The company uses this data for personalization, improving products, ad targeting, measurement and analytics, research and development, and promoting safety and security. In addition to the summary of the data policy, the text also lists all the things users give the company access to, including personal information, connections and activities on the platform, location-related information, device information, online behavior and interactions with ads and content, survey and research responses, websites visited and ads seen off the platform, and more. Furthermore, the text mentions that the company shares information with third-party partners for product improvement and services but does not sell user information. There is also an emphasis on the company\'s commitment to privacy and users\' ability to access, rectify, port, and erase their data. Overall, the text provides a detailed and comprehensive overview of Meta\'s data policy and the user data the company has access to.',
        'snapchat': 'Snap Inc. is a technology company that offers various products and services, including Snapchat, Bitmoji, and Spectacles. When users use these services, they share information with the company. The three categories of information collected are information provided by users, information obtained through service usage, and information obtained from third parties. Users give Snapchat access to a wide range of information, including personal details, content created and shared on the platform, device information, location information, and information collected through cookies and other technologies. The company uses this information for various purposes, such as improving their products and services, personalizing advertising, enhancing user experience, conducting research, and enforcing their policies. User information may be shared with other Snapchatters, business partners, and the general public. Users also have control over their information through tools such as accessing, correcting, and deleting their information, modifying advertising preferences, and controlling communication with other Snapchatters. The company collects and processes personal information in the United States and other countries outside of the user\'s location.',
        'tiktok': 'TikTok collects various types of personal information from its users, including account and profile information, user-generated content, messages, device information, purchase information, and more. Users give the company access to their contact and account information, activity on and off the platform, email or other login/device information, and cookies. This information is used for purposes such as advertising, personalized content, technology improvement, sales and purchases, user support, and more. TikTok may share user information with service providers, business partners, and within its corporate group. In the event of a sale, merger, or other business transfer, all collected information may be shared. The company may also disclose information for legal reasons. Users have the right to know, access, correct, or delete their personal information collected by TikTok, and they can update their account information and request copies of their data. They can also opt-out of targeted advertising and manage third-party advertising preferences. TikTok retains user information for as long as necessary to provide the platform and for other purposes like improving and developing the platform. The company may transmit user data to servers or data centers outside of the United States. For children\'s privacy, TikTok provides a separate experience, collects limited information, and deletes any information collected from a child. California residents have additional rights to request information and removal of user content posted by users under the age of 18.',
        'twitter': 'When users access Twitter, they provide the company with various types of information. This includes personal information such as name, email, and phone number, as well as user-generated content like tweets, posts, photos, and videos. Twitter also collects IP address and device information, location information, contacts and address book (if imported), social media connections and interactions, payment information (for purchases made on Twitter), user settings and preferences, advertising preferences and interests, and communication history with Twitter. In addition to these, Twitter also receives information from third-party online products and services, ad partners, other Twitter users, developers, and partners, corporate affiliates, and other services linked to the user\'s Twitter account. Twitter uses this information to operate, improve, and personalize their services, provide relevant content and ads, measure ad effectiveness, and enable cross-service features. The company may also share user information with payment services providers, service providers for hosting blogs and wikis, fraud detection services, advertisers, third-party content and integration providers, API and embed providers, individuals and companies not affiliated with Twitter, and in cases where required by law or in the public interest. Twitter retains user data for as long as necessary and provides privacy tools and controls to users. They also transfer user data across borders and utilize measures like standard contractual clauses to protect data rights. Twitter is not intended for users under the age of 13, and users must be old enough to consent to the processing of their personal data.',
        'netflix': 'Netflix collects and stores information about its users, including personal information such as name, email address, address, payment method, and telephone number. They also collect information about user activity on the Netflix service, interactions with customer service, device information, and information collected through cookies and other technologies. Netflix uses this information to provide, analyze, administer, personalize, and enhance their services and marketing efforts. They also use the information to select and measure the effectiveness of advertisements, communicate with users, protect user accounts and prevent fraud, and improve their service. Netflix may disclose user information to other companies and third parties for certain purposes, such as providing services on their behalf, coordinating with partners, selecting advertisements, and protecting the rights and safety of Netflix and its users. Users can choose to disclose their information through certain features of the service, such as sharing information through email, text message, and social sharing applications. Netflix provides access to user accounts and profiles, including a "Remember me" function for easy access, the ability to give others access to the account, and the option to create multiple profiles with separate watch histories. Users can also remove device access to their Netflix account. It\'s important for users to be aware of the privacy implications and security of their account information and to use the available settings and controls to manage their privacy preferences.',
        'apple': 'By using Apple products and services, users give the company access to their personal data, including but not limited to: 1. Financial offerings 2. Government ID Data (in certain jurisdictions) 3. Other information provided to Apple, including interactions with customer support and social media contacts 4. Personal data received from other sources, such as individuals, businesses or third parties acting at the user\'s direction, partners working with Apple, and other lawful sources Apple uses this data for various purposes, including powering their services, processing transactions, communicating with users, ensuring security and fraud prevention, and complying with the law. They may also use personal data for other purposes with the user\'s consent or if it is necessary to fulfill a contract, protect vital interests, or for legitimate interests. Apple may share personal data with third-party service providers and partners for purposes such as payment processing, customer support, and advertising. Apple takes measures to protect personal data through administrative, technical, and physical safeguards. Users have privacy rights, including the right to know, access, correct, transfer, restrict the processing of, and delete their personal data. They also have the right not to be treated in a discriminatory way and have the right to withdraw consent to the processing of their data. Users can exercise these privacy rights through the Apple Data and Privacy page or by contacting Apple directly. They can also opt out of receiving personalized ads through their device settings. Overall, Apple collects and processes personal data to provide and improve their products and services while ensuring the privacy and security of their users.',
        'google': 'Google collects various types of information including personal information, activity information, content created or uploaded, and data about how often the user uses their services. They may also collect identifiers such as name and phone number, demographic information, commercial information, biometric information, and internet, network, and activity information. The company uses this information for personalization, providing and improving services, serving targeted ads, and complying with applicable laws. The user also gives the company access to their Google Account information, interaction data with Google services, activity on third-party sites and apps using Google services, geolocation data, audio and visual information, communication data, health information if provided, professional and education information, and other content created or shared. The user\'s information may be shared with service providers, trusted businesses, domain administrators, and law enforcement or other third parties for legal reasons. The user has rights to access, manage, and delete their information and control personalized ads through privacy controls. The company uses technologies such as cookies, web storage, and pixel tags for data storage and tracking user activities. They may also collect server logs, use unique identifiers for security and customization purposes, and collect sensitive personal information.',
    }

    summary = summary_text.get(company.lower(), 'No summary available for this company.')

    return summary

# Main entry point
if __name__ == '__main__':
    # Use the PORT environment variable if available, otherwise use 5000 for local dev
    port = int(os.environ.get('PORT', 5000))
    # Start flask dev server
    app.run(host='0.0.0.0', port=port)
