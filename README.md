# ApproveOrRejectBot

ApproveOrRejectBot is a Telegram bot designed to streamline document submission and review processes. Users can send documents for review, and administrator can easily accept or reject submissions. Notifications keep users updated on the status of their documents, ensuring an efficient and organized workflow.

## Features

- **Document Submission:**
  - Users can submit documents in various formats including PNG, JPEG, PDF, DOCX, and more.

- **Admin Review:**
  - Administrator is notified of new document submissions.
  - Admin can review documents directly within Telegram.

- **Approval or Rejection:**
  - Admin can accept or reject documents.
  - Users receive notifications about the status of their documents.
  - If rejected, users are given feedback on why their document was not accepted.

- **User Notifications:**
  - Users receive real-time updates on their document status.
  - Notifications include whether the document is pending, approved, or rejected.

- **User-Friendly:**
  - Intuitive commands for both users and administrator.
  - Easy to navigate interface for document submission and review.

## Commands

- `/start` - Initiate interaction with ApproveOrRejectBot.
- `/stat` - View your document submission statistics. Users can see the number of documents submitted and approved.
- `/adminstat` - {admin command} View admin-specific statistics. Administrators can see overall statistics for each user, including the number of documents reviewed and the number of approvals.
- `/vipe` - {admin command} Reset the statistics for users.
- `/lang` - Change the language of the bot interface.
- `/help` - Get a list of available commands and usage instructions.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/hinderss/ApproveOrRejectBot.git
   cd ApproveOrRejectBot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Note: This project uses aiogram==3.1.1. Make sure you have this specific version installed for compatibility.

3. Set up environment variables:

   Create a `.env` file in the root directory of the project and add the following variables:
   ```plaintext
   BOT_TOKEN="your_telegram_bot_token"
   ADMIN_CHAT_ID="your_admin_chat_id"
   SQLALCHEMY_DATABASE_URI=sqlite+aiosqlite:///instance/data.db
   LANGUAGES_INI=app/language/languages.ini
   ```

   Alternatively, you can export these variables in your shell environment:
   ```bash
   export BOT_TOKEN="your_telegram_bot_token"
   export ADMIN_CHAT_ID="your_admin_chat_id"
   export SQLALCHEMY_DATABASE_URI=sqlite+aiosqlite:///instance/data.db
   export LANGUAGES_INI=app/language/languages.ini 
   ```
   
   Tips:
   - You can register your bot and get the `BOT_TOKEN` from [BotFather](https://t.me/BotFather).
   - You can get your `ADMIN_CHAT_ID` using [Get My ID bot](https://t.me/getmyid_bot).

4. Run the bot:
   ```bash
   python bot.py
   ```

## Usage

1. Start the bot by sending the `/start` command.
2. Submit the documents by simply sending them to the bot.
3. Admins can review submissions and either accept or reject them.
4. Users will receive notifications about the status of their submissions.
5. Administrators can change their decision later.

## Contributing

We welcome contributions! Please fork the repository and submit pull requests for any improvements or bug fixes.