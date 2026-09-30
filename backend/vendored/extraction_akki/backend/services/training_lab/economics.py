"""Explicit assumptions, discounted value and falsifiable forecast scoring."""
import math


def value_case(*,monthly_benefit,monthly_cost,setup_cost,adoption_probability,delay_months,horizon_months,annual_discount_rate,next_best_npv):
    numeric=(monthly_benefit,monthly_cost,setup_cost,adoption_probability,annual_discount_rate,next_best_npv)
    if any(not math.isfinite(x) for x in numeric) or min(monthly_benefit,monthly_cost,setup_cost,annual_discount_rate)<0 or not 0<=adoption_probability<=1:
        raise ValueError('Finite, nonnegative costs and valid adoption probability required')
    if not 1<=horizon_months<=120 or not 0<=delay_months<=horizon_months:
        raise ValueError('Invalid horizon or delivery delay')
    rate=(1+annual_discount_rate)**(1/12)-1
    npv=-setup_cost; break_even=None
    for month in range(1,horizon_months+1):
        # Operational cost incurred after launch even if adoption underperforms.
        net=(monthly_benefit*adoption_probability-monthly_cost) if month>delay_months else 0
        npv += net/(1+rate)**month
        if npv>=0 and break_even is None: break_even=month
    return {'risk_adjusted_npv':round(npv,2),'break_even_month':break_even,
            'next_best_npv':next_best_npv,'incremental_npv':round(npv-next_best_npv,2),
            'preferred_on_supplied_assumptions':npv>max(0,next_best_npv),
            'evidence_class':'scenario_estimate_not_investment_approval','currency':'caller_consistent_units',
            'limitations':'Constant monthly flows; adoption probability and costs are caller assumptions, not measured forecasts.'}


def score_predictions(predictions):
    scored=[]
    for p in predictions:
        low,high,actual=p['low'],p['high'],p['actual']
        if not all(math.isfinite(v) for v in (low,high,actual)) or low>high:
            raise ValueError('Finite ordered prediction range and actual required')
        if not p['prediction_ref'] or not p['actual_ref'] or p['prediction_ref']==p['actual_ref']:
            raise ValueError('Distinct prediction and measured-actual references required')
        scored.append({**p,'within_predicted_range':low<=actual<=high,
                       'absolute_midpoint_error':abs(actual-(low+high)/2)})
    return {'predictions':scored,'coverage':sum(p['within_predicted_range'] for p in scored)/len(scored),
            'evidence_class':'caller_supplied_refs_not_independently_verified','automatic_prior_update':False,
            'limitations':'Forecast must have been recorded before actuals. References alone do not establish chronology or causation.'}