from langchain.evaluation import load_evaluator
from langchainn import chat_with_bot
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os


#9 quick answer
questions_and_answers = [
    {
        "input": "How do I use Composer's command line?",
        "reference": "Usage: composer [OPTIONS..] [--] [FILES..]. Asiga Composer version 1.2.12 built Tue Oct 20 2020. Options include --version, --help, --headless, and many others. The options help & version are consistent across versions. Supported files include *.combld, *.zip, *.printRequest, *.ply, *.stl, and *.slc. Download the latest version from www.asiga.com."
    },
    {
        "input": "Tell me about the fast print mode in Composer.",
        "reference": "The fast print mode will move the platform more quickly when possible and enable separation detect by default. It does not affect the accuracy of the printing. Separation detect will use the encoders to determine when the print has detached from the film. If it is off, the platform will rise more to ensure detachment, which will also ensure resin will flow completely under the printed model. It's always safe to enable the Fast Print Mode, but the Separation Detect should be disabled for a test if you encounter print issues."
    },
    {
        "input": "How do I add a new material ini file in Composer?",
        "reference": "To import a new material ini file, make a folder on your desktop or document folder and put the material ini file in there. This folder can be used for multiple ini files. Open Composer, click on new. Click on the gear icon on the right. Select preferences, and the tab Materials will open. Press the + symbol to navigate to the folder which will add it to the list. Click select folder, then ok. You can then select it under the materials tab. If your printer is a 385nm printer and you're using a resin for a 405nm projector, it may not show up or be greyed out unless you select a 405nm printer to print with."
    },
    {
        "input": "Which external radiometers does Asiga recommend?",
        "reference": "Asiga recommends two external radiometers. One is from International Lights, which can be found at https://www.intl-lighttech.com/products/asiga-ilt2445. The other is the Opsytec Dr.Groebel RM-12, model 'UVA+', which can be found at https://www.opsytec.com/products/radiometer/rm-12. Asiga does not sell the radiometers; they need to be purchased directly from the manufacturers."
    },
    {
        "input": "My printer shows an 'LED Light Intensity Too Low' error. What should I do?",
        "reference": "The LED Light Intensity Too Low can sometimes be a firmware bug. Shutting down the printer or restarting it might fix this error message. If the error is recurring, obtain the Debug Information and Error Log of your machine right after seeing the message, without restarting. Access this through Composer's web interface in the System Information tab. Please also ensure that you're running the latest firmware and Composer version. You can download the latest version from https://www.asiga.com/accounts/software/ and ensure you are using the latest material ini files from the Asiga page."
    },
    {
        "input": "My print has incomplete supports. What could be the issue?",
        "reference": "The image you provided shows multiple problems. In one picture, the detachment might be due to incorrect platform calibration. In another, supports are incomplete. Adjust support settings to make supports 4mm long, with a spacing of 2mm, and a contact width of 0.6mm - 0.7mm."
    },
    {
        "input": "How do I check power-related parts for damage on PRO4K?",
        "reference": "Check the Q1 chip on the power board for any signs of thermal damage. Ensure both connectors for the projector power on the power board are intact. Examine both projector power cables for thermal damage. Verify the two big green connectors do not show thermal damage. Check if the wires between the two green connectors are slightly loose."
    },
    {
        "input": "My PRO4K's LCD screen is displaying content backwards. What should I do?",
        "reference": "This is occasionally a timing issue between the LCD screen and the computer board. Restarting the printer should resolve the issue."
    },
    {
        "input": "The parts I printed with PRO4K are not the right size. What could be the issue?",
        "reference": "Check the resin you're printing with. Verify if you're checking the fit post-curing as it may affect sizing. Avoid trapped volume on hollow models. Ensure proper clearance is added during CAD design. Check if a DME file is available for your dental software at https://myaccount.asiga.com/accounts/#tab_software. To check the printer, ensure the basin glass is clean, check the focus image for sharpness, and ensure there's no change in sharpness when refreshing the image."
    }
]

#11 more support website & user guide
questions_and_answers.extend([
    {
        "input": "How do I access the PRO 4K's web interface?",
        "reference": "Access the printer's web interface by connecting the printer to your network. You can auto-detect in Composer by selecting 'New', choosing your target printer, and clicking on the Earth Icon. Alternatively, if you know the IP address or printer name, you can type it into your web browser's address bar. Format: http://<printer name or IP address> and then press enter."
    },
    {
        "input": "What does the build queue in PRO 4K's web interface show?",
        "reference": "The build queue provides an overview of print jobs queued in your printer. It's a tool that lets you manage and prioritize your print jobs."
    },
    {
        "input": "What's the purpose of the front panel on the PRO 4K web interface?",
        "reference": "The front panel allows you to view in real time what your printer is doing. Moreover, it can act as a remote control allowing you to manage and control the printer from your desk."
    },
    {
        "input": "Can I change the build extents on the PRO 4K?",
        "reference": "In the settings tab, you can view your printer’s build extents and hide certain menu features. It's useful in a production environment. However, Asiga does not advise modifying the build extents without supervision from an authorized reseller or Asiga. Changing the build extents can result in a loss of accuracy."
    },
    {
        "input": "How do I gather system information from the PRO 4K?",
        "reference": "System information provides operational details on your printer like printer name and uptime. Most importantly, it grants access to all the printer logs including Debug Information, Error log, Buildlog, and Printer ini. These logs can be crucial for technical support requests."
    },
    {
        "input": "How do I update the firmware on the PRO 4K?",
        "reference": "To update the firmware, download the latest version for the PRO 4K. In the web interface, click 'choose file', navigate to the downloaded file, and upload. Once done, the printer will automatically restart, completing the firmware update process."
    },
    {
        "input": "Where can I find the user guide for the MAX 3D printer?",
        "reference": "The MAX user guide is available at this link: https://drive.google.com/file/d/100U0qrx9nkFV1743zDEbM1WuIzU-2L4s/view?usp=share_link"
    },
    {
        "input": "I'm having issues with Composer, where can I find troubleshooting information?",
        "reference": "For problems related to Composer, consult the Composer Troubleshooting Guide at this link: https://drive.google.com/file/d/141Azcx6cviJa3pO8ksoZLBAbYsr-BP3C/view?usp=share_link"
    },
    {
        "input": "Is there a specific guide for the PRO 4K 3D printer?",
        "reference": "Yes, the PRO 4K user guide can be found here: https://drive.google.com/file/d/1tQVdOX8gNeEuU8HanaMuPLMITIFRbYtv/view?usp=share_link"
    },
    {
        "input": "How do I prevent light scattering in my prints?",
        "reference": "Light scattering, which results in extra cured material on your prints, is often caused by obstacles like dirty optics. Ensure the basin glass is clean and the build tray is not damaged. Periodic maintenance and checking for smudges or cured resin can help reduce this effect."
    },
    {
        "input": "Why is it important to maintain the build tray?",
        "reference": "A damaged or stretched out build tray can lead to print issues. It's essential to maintain the build tray for optimal performance. Consider replacing it if damaged to avoid misprints."
    }
])

accuracy_criteria = {
    "accuracy": """
Score 1: The answer is completely unrelated to the reference.
Score 3: The answer has minor relevance but does not align with the reference.
Score 5: The answer has moderate relevance but contains inaccuracies.
Score 7: The answer aligns with the reference but has minor errors or omissions.
Score 10: The answer is completely accurate and aligns perfectly with the reference."""
}

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

evaluator = load_evaluator(
    "labeled_score_string", 
    criteria=accuracy_criteria, 
    llm=ChatOpenAI(model="gpt-3.5-turbo-16k"),
)

sum_scores = 0
total_responses = len(questions_and_answers)
q = 1

for qna in questions_and_answers:
    input_question = qna["input"]
    reference_answer = qna["reference"]
    chatbot_response = chat_with_bot(input_question)
    
    eval_result = evaluator.evaluate_strings(
        prediction=chatbot_response,
        reference=reference_answer,
        input=input_question
    )
    
    score = eval_result['score']
    sum_scores += score
    
    print(f"Question Number: {q}")
    q+=1

# Calculate average score
average_score = sum_scores / total_responses
print('-----------------------------------------------')
print(f"Average Score (Accuracy): {average_score:.2f} out of 10")
print('-----------------------------------------------')


# Question Number: 20
# -----------------------------------------------
# Average Score (Accuracy): 8.05 out of 10
# -----------------------------------------------
