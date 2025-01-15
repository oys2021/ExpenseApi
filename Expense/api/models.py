from django.db import models
from django.contrib.auth.models import AbstractUser


class Customuser(AbstractUser):
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    phone=models.CharField(max_length=15,null=True,blank=True)

    def __str__(self):
        return self.username

class Wallet(models.Model):
    name=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    balance=models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
    user=models.ForeignKey(Customuser,on_delete=models.CASCADE)
    image= models.ImageField(upload_to='wallet_images/', null=True,blank=True, max_length=100)
    
        
    def __str__(self):
        return self.name
    
    
class TransactionType(models.Model):
    Transaction_Types=[
        ("Income","Income"),
        ("Expense","Expense")
    ]
    name=models.CharField(max_length=30,choices=Transaction_Types)  

    def __str__(self):
        return self.name
    
class TransactionCategory(models.Model):
    name=models.CharField(max_length=30)
    transaction_type=models.ForeignKey(TransactionType,on_delete=models.CASCADE) 
    
    def __str__(self):
        return f"{self.name} ({self.transaction_type.name})"
    
class Transaction(models.Model):
    transaction_type=models.ForeignKey(TransactionType,on_delete=models.CASCADE,related_name="transactions")
    transaction_category=models.ForeignKey(TransactionCategory,on_delete=models.CASCADE,related_name="transactions")
    date=models.DateTimeField()
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(Customuser, on_delete=models.CASCADE, related_name="transactions")
    wallet=models.ForeignKey(Wallet,on_delete=models.CASCADE,related_name="wallet")
    
    def save(self, *args, **kwargs):
        if self.transaction_category.transaction_type != self.transaction_type:
            raise ValueError("Transaction types do not match")
        
        if self.transaction_type.name == "Income":
            self.wallet.balance += self.amount
        elif self.transaction_type.name == "Expense":
            self.wallet.balance -= self.amount
        else:
            raise ValueError("Invalid transaction type")

        self.wallet.save()

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.amount} - {self.transaction_category.name} ({self.transaction_type.name})"
    

    