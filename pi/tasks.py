from .models import PiPayment
from django.utils.timezone import now
from stellar_sdk import Server, Asset, Keypair, TransactionBuilder, Network
from mnemonic import Mnemonic
from .keyfunc import account_keypair
import time

def process_payment_task(pi_amount, seed, destination):
    try:
        start_time = time.time() 
        my_seed_phrase = seed
        des_address = destination
        amount = pi_amount

        # Stellar payment processing logic
        my_language = 'english'
        mnemo = Mnemonic(my_language)

        if mnemo.check(my_seed_phrase):
            binary_seed = Mnemonic.to_seed(my_seed_phrase)
            account_number = 0
            kp = account_keypair(binary_seed, account_number)

            source_keypair = Keypair.from_secret(kp.secret)
            server = Server("https://api.mainnet.minepi.com/")
            source_account = server.load_account(source_keypair.public_key)
            base_fee = server.fetch_base_fee()

            transaction = (
                TransactionBuilder(
                    source_account=source_account,
                    network_passphrase="Pi Network",
                    base_fee=base_fee,
                )
                .append_payment_op(des_address, asset=Asset.native(), amount=str(amount))
                .set_timeout(300)
                .build()
            )
            transaction.sign(source_keypair)
            server.submit_transaction(transaction)
        end_time = time.time()
        operation_time = end_time - start_time

        
        print(f"Operation Time: {operation_time:.2f} seconds")
    except:
        print(f"An Error occured")
