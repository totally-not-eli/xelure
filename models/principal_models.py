from sqlalchemy import (
    Integer,
    String,
    TIMESTAMP,
    Text,
    Date,
    Float,
    DATETIME,
    Column,
    ForeignKey,
    SmallInteger,
    Numeric,
    Boolean
)
from sqlalchemy.orm import relationship

from models.base import Base

class Principal(Base):
    __tablename__ = "principal"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    total_principal_funds_available = Column(Float)
    month = Column(Date)
    
class LoanData(Base):
    __tablename__ = 'loan_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(Integer)
    investor_loan_ = Column(String)
    servicer_loan_ = Column(String)
    pool_ = Column(String)
    subpool_ = Column(String)
    distribution_date = Column(Date, nullable=True)
    paid_to_date = Column(Date, nullable=True)
    advance_paid_to_date = Column(Date, nullable=True)
    scheduled_gross_interest = Column(Numeric(precision=17, scale=2))
    master_servicing_fee = Column(Numeric(precision=17, scale=2))
    servicing_fee = Column(Numeric(precision=17, scale=2))
    trustee_fee = Column(Numeric(precision=17, scale=2))
    insurance_fee = Column(Numeric(precision=17, scale=2))
    special_servicing_fee = Column(Numeric(precision=17, scale=2))
    scheduled_net_interest = Column(Numeric(precision=17, scale=2))
    other_fees = Column(Numeric(precision=17, scale=2))
    beginning_scheduled_balance = Column(Numeric(precision=17, scale=2))
    ending_scheduled_balance = Column(Numeric(precision=17, scale=2))
    beginning_actual__balance = Column(Numeric(precision=17, scale=2))
    ending_actual__balance = Column(Numeric(precision=17, scale=2))
    scheduled_principal = Column(Numeric(precision=17, scale=2))
    curtailments = Column(Numeric(precision=17, scale=2))
    curtailment_adjustments = Column(Numeric(precision=17, scale=2))
    other_principal_adjustments = Column(Numeric(precision=17, scale=2))
    curtailment_date = Column(Date, nullable=True)
    pif_type = Column(String)
    pif_date = Column(Date, nullable=True)
    prepayment = Column(Float)
    repurchase_principal = Column(Numeric(precision=17, scale=2))
    liquidation_principal = Column(Numeric(precision=17, scale=2))
    principal_recoveries = Column(Numeric(precision=17, scale=2))
    interest_recoveries = Column(Numeric(precision=17, scale=2))
    total_recoveries = Column(Numeric(precision=17, scale=2))
    principal_losses = Column(Numeric(precision=17, scale=2))
    interest_losses = Column(Numeric(precision=17, scale=2))
    total_losses = Column(Numeric(precision=17, scale=2))
    ppis = Column(Numeric(precision=17, scale=2))
    ppie = Column(Numeric(precision=17, scale=2))
    sscra_shorfalls = Column(Numeric(precision=17, scale=2))
    other_interest_adjustments = Column(Numeric(precision=17, scale=2))
    principal_advances = Column(Numeric(precision=17, scale=2))
    interest_advances = Column(Numeric(precision=17, scale=2))
    stop_advance_flag = Column(Boolean)
    stop_advance_principal = Column(Numeric(precision=17, scale=2))
    stop_advance_interest = Column(Numeric(precision=17, scale=2))
    total_stop_advance = Column(Numeric(precision=17, scale=2))
    current_pi_constant = Column(Numeric(precision=17, scale=2))
    special_hazard_losses = Column(Numeric(precision=17, scale=2))
    fraud_losses = Column(Numeric(precision=17, scale=2))
    bankruptcy_losses = Column(Numeric(precision=17, scale=2))
    delinquency_status = Column(String)
    reo_date = Column(Date, nullable=True)
    reo_balance = Column(Numeric(precision=17, scale=2))
    reo_book_value = Column(Numeric(precision=17, scale=2))
    loan_status = Column(String)
    neg_am = Column(Float)
    prepay_penaltyym = Column(Float)
    prepay_penaltyym_waived = Column(Float)
    current_note_rate = Column(Numeric(precision=17, scale=2))
    next_note_rate = Column(Numeric(precision=17, scale=2))
    current_net_note_rate = Column(Numeric(precision=17, scale=2))
    next_net_note_rate = Column(Numeric(precision=17, scale=2))
    next_rate_adjustment_date = Column(Date, nullable=True)
    next_payment_adjustment_date = Column(Date, nullable=True)
    remaining_term = Column(Integer)
    modification_flag = Column(Boolean)
    modification_date = Column(Date, nullable=True)
    beginning_deferred_balance = Column(Numeric(precision=17, scale=2))
    ending_deferred_balance = Column(Numeric(precision=17, scale=2))
