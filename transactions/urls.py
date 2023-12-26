from django.urls import path
from .views import DepositMoneyView,WithdrawMoneyView,LoanMoneyView,TransactionReportView,PayLoanView,LoanListView

urlpatterns=[
    path('deposit/',DepositMoneyView.as_view(), name='deposit_money'),
    path('withdraw/',WithdrawMoneyView.as_view(), name='withdraw_money'),
    path('loan/',LoanMoneyView.as_view(), name='loan_money'),
    path('loan/pay/',PayLoanView.as_view(), name='pay_loan'),
    path('loan/list/',LoanListView.as_view(), name='loan_list'),
    path('report/',TransactionReportView.as_view(), name='transaction_report'),
]