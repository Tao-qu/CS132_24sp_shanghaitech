<h1> BANKING SYSTEM REQUIREMENT DOCUMENT</h1>
<h5 align='right'>Team 5</h5>
<h2>Contents</h2>
1. Introduction of Product<br/>
2. Domain Analyses<br/>
3. Specific Requirements<br/>
<h3>Introduction of Product</h3>
In this project, we are developing a software that can manage bank card accounts, which includes querying account, withdrawing and depositing cash, transferring properties to other accounts and so on. By creating a database of the data of all accounts, the system guarantees the fluency and correctness of property transfers.

<h3>Domain Analyses</h3>
<h5>Class Diagram</h5>
Here is the class diagram, which represents the structure of the system:
<img src=./img/BankingSystemClassDiagram.png>
The data of each account includes User ID(which can be replaced by phone number or others), user password, card ID, number of cards owned, the ID, password and deposit of each card owned. Also, state parameters like whether your account is logged in will be stored.
<h5>Use Case Diagram</h5>
The use case diagram shows the usage of the system and ways of interaction between human and system.
<img src=./img/BankingSystemUseCaseDiagram.png>
What people can do via the system is shown. There are two respect interfaces. Through the ATM system, people can query their accounts, deposit and withdraw the cash. In the APP system, they are able to create a personnal account and connect it with cards. They're able to reset the password when identity is confirmed. They can search for detailed information about their own accounts, as well as transferring their deposit. 
<h5>Activity Diagram</h5>
The activity diagram displays the detailed procedures of interactions.
<img src=./img/BankingSystemActivityDiagram.png>
When withdrawing, recharging or transferring deposit, several items must be verified: valid card ID and password and valid amount. It's better if there is a confirmation for users before done deal.
<h3>Specific Requirements</h3>

#### ATM Functionality Requirements

**R1.1 Create Account**  
The ATM system shall provide the capability for users to create a new bank account. During the creation process, users must set a password to ensure security. The system will guide the user through necessary steps, including personal information verification and security setup.

**R1.2 Close Account**  
The ATM system shall allow users to close their bank account permanently. This feature ensures all funds are transferred out and the user confirms the closure to prevent accidental terminations.

**R1.3 Insert Card**  
The ATM must identify and verify a user’s banking card upon insertion. This process requires the card number for authentication.

**R1.4 Return Card**  
The ATM shall return the user's card after the completion of transactions or upon user request, ensuring no card retention post-session.

**R1.5 Deposit Cash**  
Users shall be able to deposit cash into their accounts at the ATM, with immediate verification and account balance updating.

**R1.6 Withdraw Cash**  
The ATM system shall enable cash withdrawals, requiring user authentication via password and allowing the user to specify withdrawal amounts.

**R1.7 Change Password**  
The ATM shall facilitate password changes for user accounts, guiding users through a secure process to set a new password.

**R1.8 Transfer Money**  
The ATM system shall support money transfers to another user's account, requiring the receiver's account ID and specified transfer amount.

**R1.9 Query Transactions**  
The ATM must provide a facility for users to query and review their transaction history, displaying detailed account activities.

### App Functionality Requirements

**R2.1 Log In**  
The banking app shall support user login using an ID and password. This feature may also support multiple application interfaces (app_id) for enhanced compatibility.

**R2.2 Log Out**  
The app shall facilitate a secure log out, terminating the user’s session on the current device or app specified by app_id.

**R2.3 Close App**  
The system shall allow users to close the banking application securely on their device, ensuring all sessions are properly terminated.

**R2.4 Change Password**  
The app shall provide a feature for password change, ensuring the process is secure and possibly requiring re-authentication for enhanced security.

**R2.5 Transfer Money**  
Within the app, users shall be able to transfer money by specifying the recipient’s account ID and the amount. Additional verification may be required for security purposes.

**R2.6 Query Transactions**  
The app shall allow users to access and review their transaction history, providing a clear and detailed display of all transactions made through the app.

