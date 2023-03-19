window.onload = function(){
    const register_btn = document.getElementById('register_button');
    register_btn.addEventListener('click', try_register, false);

    const logout_btn = document.getElementById('logout_button');
    logout_btn.addEventListener('click', logout, false);

// const connect_wallet_button = document.getElementById('connect_wallet_button');
// connect_wallet_button.addEventListener('click', try_connect_wallet, false);

// const gen_wallet_button = document.getElementById('gen_wallet_button');
// gen_wallet_button.addEventListener('click', gen_wallet, false);

// const transaction_button = document.getElementById('transaction_button');
// transaction_button.addEventListener('click', do_transaction, false);
};


const data64 = "ewogICAgInB1YmxpY19rZXkiOiAiRURERDMyRUExOEQxMEIxNjRFMkM2QzMxQjU4RDc4OEYwMkZFRUE3NkRCN0ZDNjNCQTBFMjQyN0ZBMDFDMEI2NEY3IiwKICAgICJwcml2YXRlX2tleSI6ICJFREE4NEVEOEYyNTQ0MUVFMTFFNDc5MTFEQTU1NzQwRjkwQTAyMEI1RTMxMzJBOUIyRDQzMDU5MTQ4NEEyQUNDMTQiLAogICAgImNsYXNzaWNfYWRkcmVzcyI6ICJyaDV5dlFtS0tTNFFSdUU0aDdSWFBleW0yUHpuc3M3YVJMIiwKICAgICJzZWVkIjogInNFZFNZZTVkckhXUFRIZm8xSmpOWW02bTlvY1cxRTQiCn0="
     
function try_register() {
  console.log("Trying to register!");

  // var xhr = new XMLHttpRequest();
  // xhr.onreadystatechange = function () {
  //   if (this.readyState != 4) return;

  //   if (this.status == 201) {
        var data = JSON.parse(atob(data64));

        if (data.seed !== null) {
          console.log("Logged in");
         // localStorage.setItem('access_token', JSON.stringify(data.jwt));
          document.getElementById("login_container").style.display = "none";
          document.getElementById("wallet_container").style.display = "block";
          document.getElementById('logout_button').style.display = "block";

          // Generating keys
          // var xhrKeys = new XMLHttpRequest();
          // xhrKeys.onreadystatechange = function () {
          //   if (this.readyState != 4) return;
          //   if (this.status == 200) {
          //     var keys = JSON.parse(this.responseText);
          //     console.log(keys);
          //   } else {
          //     console.log("Generate keys: Something went wrong");
          //   }
          // };

          // xhrKeys.open("POST", "/api/account/generate_keys/");
          // xhrKeys.setRequestHeader("Content-Type", "application/json");
          // xhrKeys.send();

          // Set values
          // document.getElementById("wallet_info_seed").innerHTML = `Seed: ${data.seed}`;
          document.getElementById("wallet_info_address").innerHTML = `Address: ${data.classic_address}`;
          // document.getElementById("wallet_info_pub_key").innerHTML = `Public key: ${data.public_key}`;
          // document.getElementById("wallet_info_priv_key").innerHTML = `Private key: ${data.private_key}`;
          document.getElementById("wallet_info_link").href = `https://testnet.xrpl.org/accounts/${data.classic_address}`;

        // } else {
        //   console.log("Registration: Something went wrong");
        //   // popup
        //   document.getElementById("some_error").style.display = "block";
        //   setTimeout(function() { 
        //       document.getElementById("some_error").style.display = "none";
        //     }, 2000);
        // }
        }

        //};

  // xhr.open("POST", "http://127.0.0.1:8000/api/account/");
  // xhr.setRequestHeader("Content-Type", "application/json");
  // xhr.send();
}

function logout() {
  document.getElementById("login_container").style.display = "block";
  document.getElementById("wallet_container").style.display = "none";
 // document.getElementById("transaction_container").style.display = "none";
  localStorage.clear();
  document.getElementById('logout_button').style.display = "none";
}

function perform_transaction(channel) {
	console.log("Received request to pay");
	do_channel_transaction(channel);
} 

// PAGE: WALLET
async function try_connect_wallet() {
  seed = document.getElementById('seed_input').value;
  console.log(`Trying to connect existing wallet with seed: ${seed}`);

  const client = new xrpl.Client("wss://s.altnet.rippletest.net:51233")
  await client.connect();
  console.log("Client connected");
  console.log("Testing wallet");

  wallet = xrpl.Wallet.fromSeed(seed);

  const response = await client.request({
      "command": "account_info",
      "account": wallet.address,
      "ledger_index": "validated"
  });

  console.log(`Wallet tested successfully, here is it:`); 
  console.log(response);

  localStorage.setItem('seed', JSON.stringify(seed));
  document.getElementById("wallet_container").style.display = "none";
  document.getElementById("transaction_container").style.display = "block";

  document.getElementById("wallet_info_seed").innerHTML = `Seed: ${seed}`;
  document.getElementById("wallet_info_address").innerHTML = `Address: ${wallet.address}`;
  document.getElementById("wallet_info_balance").innerHTML = `Balance: ${response.result.account_data.Balance}`;
  document.getElementById("wallet_info_link").href = `https://testnet.xrpl.org/accounts/${wallet.address}`;
}

async function gen_wallet() {
  console.log("Trying to generate wallet");
  const client = new xrpl.Client("wss://s.altnet.rippletest.net:51233");
  await client.connect();
  console.log("Client connected");
  console.log("Funding and testing wallet");

  const fund_result = await client.fundWallet();
  const test_wallet = fund_result.wallet;

  const response = await client.request({
    "command": "account_info",
    "account": test_wallet.address,
    "ledger_index": "validated"
  })
  console.log(`Wallet tested successfully, here is it:`); 
  console.log(response);

  localStorage.setItem('seed', JSON.stringify(test_wallet.seed));
  document.getElementById("wallet_container").style.display = "none";
  document.getElementById("transaction_container").style.display = "block";

  document.getElementById("wallet_info_seed").innerHTML = `Seed: ${test_wallet.seed}`;
  document.getElementById("wallet_info_address").innerHTML = `Address: ${test_wallet.address}`;
  document.getElementById("wallet_info_balance").innerHTML = `Balance: ${response.result.account_data.Balance}`;
  document.getElementById("wallet_info_link").href = `https://testnet.xrpl.org/accounts/${test_wallet.address}`;
}

function upload_image() {
  var file = document.getElementById("uploadedImage").files[0];
  var reader = new FileReader();
   reader.onload = function () {
     pushToIpfs(reader.result)
   };
   reader.onerror = function (error) {
     console.log('Error: ', error);
   };
   reader.readAsDataURL(file);

  var images_contatiner = document.getElementById("images_contatiner");
  images_contatiner.style.display = "block";
}

async function pushToIpfs(base64img) {
  console.log("Trying to upload img!");
  document.getElementById("loader").style.display = "block";

  var body = JSON.stringify({ "title": "My Image", "description": "The best image", "content": base64img })

  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (this.readyState != 4) return;

    if (this.status == 201) {
        var data = JSON.parse(this.responseText);

        if (data.seed !== null) {
          console.log("Image upload success");
          document.getElementById("loader").style.display = "none";
          var new_img = document.createElement("img");
          var images_list = document.getElementById("images_list");
          images_list.appendChild(new_img);
          new_img.width = 200;
          new_img.src = base64img;

        } else {
          console.log("Image upload: Something went wrong");
          // popup
          document.getElementById("some_error").style.display = "block";
          setTimeout(function() { 
              document.getElementById("some_error").style.display = "none";
            }, 2000);
        }
      }

}; 
 
  var header = data64;
  xhr.open("POST", "https://demedia.parhizkari.com/api/article/");
  xhr.setRequestHeader("X-WALLET-AUTH", header);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(body);
}

// PAGE: TRANSACTIONS

async function do_transaction() {
  console.log("Trying to do the transaction");
  
  const client = new xrpl.Client("wss://s.altnet.rippletest.net:51233")
  await client.connect();

  seed = JSON.parse(localStorage.getItem("seed"));
  test_wallet = xrpl.Wallet.fromSeed(seed);

  const prepared = await client.autofill({
    "TransactionType": "Payment",
    "Account": test_wallet.address,
    "Amount": xrpl.xrpToDrops("22"),
    "Destination": "rnR6eYwjYbCNkVXHcyw9H4UsS75HZKB4z2"
  })
  const max_ledger = prepared.LastLedgerSequence
  console.log("Prepared transaction instructions:", prepared);
  console.log("Transaction cost:", xrpl.dropsToXrp(prepared.Fee), "XRP");
  console.log("Transaction expires after ledger:", max_ledger);

  const signed = test_wallet.sign(prepared);
  console.log("Identifying hash:", signed.hash);
  console.log("Signed blob:", signed.tx_blob);

  const tx = await client.submitAndWait(signed.tx_blob);

  console.log("Transaction result:", tx.result.meta.TransactionResult);
  console.log("Balance changes:", JSON.stringify(xrpl.getBalanceChanges(tx.result.meta), null, 2));

  // Update with new balance 
  const response = await client.request({
    "command": "account_info",
    "account": test_wallet.address,
    "ledger_index": "validated"
  });
  document.getElementById("wallet_info_balance").innerHTML = `Balance: ${response.result.account_data.Balance}`;

  // popup
  document.getElementById("popup").style.display = "block";
  setTimeout(function() { 
      document.getElementById("popup").style.display = "none";
    }, 5000);
}

async function do_channel_transaction(channel) {
  console.log("Trying to do the transaction");
  
  const client = new xrpl.Client("wss://s.altnet.rippletest.net:51233")
  await client.connect();

  seed = JSON.parse(localStorage.getItem("seed"));
  test_wallet = xrpl.Wallet.fromSeed(seed);

  const prepared = await client.autofill({
    "TransactionType": "Payment",
    "Account": test_wallet.address,
    "Amount": xrpl.xrpToDrops("22"),
    "Destination": "rnR6eYwjYbCNkVXHcyw9H4UsS75HZKB4z2"
  })
  const max_ledger = prepared.LastLedgerSequence
  console.log("Prepared transaction instructions:", prepared);
  console.log("Transaction cost:", xrpl.dropsToXrp(prepared.Fee), "XRP");
  console.log("Transaction expires after ledger:", max_ledger);

  const signed = test_wallet.sign(prepared);
  console.log("Identifying hash:", signed.hash);
  console.log("Signed blob:", signed.tx_blob);

  const tx = await client.submitAndWait(signed.tx_blob);

  console.log("Transaction result:", tx.result.meta.TransactionResult);
  console.log("Balance changes:", JSON.stringify(xrpl.getBalanceChanges(tx.result.meta), null, 2));

  // Update with new balance 
  const response = await client.request({
    "command": "account_info",
    "account": test_wallet.address,
    "ledger_index": "validated"
  });
  document.getElementById("wallet_info_balance").innerHTML = `Balance: ${response.result.account_data.Balance}`;

  // popup
  document.getElementById("popup").style.display = "block";
  setTimeout(function() { 
      document.getElementById("popup").style.display = "none";
    }, 5000);


  channel.push("transaction:success", {}, 10000)
    .receive("ok", (msg) => console.log("Push transaction:success") )
    .receive("error", (reasons) => console.log("create failed", reasons) )
    .receive("timeout", () => console.log("Networking issue...") )
}


