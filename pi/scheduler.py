from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from django.utils.timezone import now
from .models import PiPayment
from stellar_sdk import Server, Asset, Keypair, TransactionBuilder, Network
from mnemonic import Mnemonic
from .keyfunc import account_keypair



def process_payment_task(payment_id):
    try:
        payment = PiPayment.objects.get(id=payment_id)

        if not payment.processed:  # Ensure the payment hasn't been processed
            my_seed_phrase = payment.seed
            des_address = payment.destination
            amount = payment.amount

            # Stellar payment processing logic
            my_language = 'english'
            mnemo = Mnemonic(my_language)

            if mnemo.check(my_seed_phrase):
                binary_seed = Mnemonic.to_seed(my_seed_phrase)
                account_number = 0
                kp = account_keypair(binary_seed, account_number)

                source_keypair = Keypair.from_secret(kp.secret)
                server = Server("https://api.testnet.minepi.com/")
                source_account = server.load_account(source_keypair.public_key)
                base_fee = server.fetch_base_fee()

                transaction = (
                    TransactionBuilder(
                        source_account=source_account,
                        network_passphrase="Pi Testnet",
                        base_fee=base_fee,
                    )
                    .append_payment_op(des_address, asset=Asset.native(), amount=str(amount))
                    .set_timeout(300)
                    .build()
                )
                transaction.sign(source_keypair)
                server.submit_transaction(transaction)
    except PiPayment.DoesNotExist:
        print(f"Payment ID {payment_id} does not exist.")



def check_scheduled_payments():
    # Get the current time
    current_time = now()
    #print(current_time)
    
    # Query the database for payments with `scheduled_time` matching the current time
    payments = PiPayment.objects.filter(scheduled_time__lte=current_time, processed=False)
    
    for payment in payments:
        process_payment_task(payment.id)  # Print 2 when the scheduled time matches
        payment.processed = True
        payment.save()# Mark the payment as processed to avoid duplicate execution


def start_scheduler():
    scheduler = BackgroundScheduler()
    
    # Add a job to check for scheduled payments every second
    scheduler.add_job(
        check_scheduled_payments,
        'interval',
        seconds=1,  # Check every second
        id="scheduled_payment_checker",
        replace_existing=True,
        max_instances=2
    )
    
    scheduler.start()
