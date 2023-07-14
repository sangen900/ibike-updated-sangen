import streamlit as st
import pandas as pd
from os import path
import os
from streamlit import session_state as ss
from modules import order, group

def render():
	
	st.title('Project Manager')
	st.markdown(
	        """
	        Your role is to generate customer orders, monitor the progress of your team members, delegate tasks, and provide constructive feedback.
	        """)
	if 'order_requested' not in ss:
		ss['order_requested'] = False
	if 'display_orders' not in ss:
		ss['display_orders'] = False
	if 'orders_full' not in ss:
		ss['orders_full'] = False

	col1, col2 = st.columns([1, 2])

	with col1:
		
		order_request = st.button('Generate New Customer Order',on_click=create_order)
		
		if ss.order_requested:
			st.write(f"A new customer order has been recieved. There are {len(ss.group_state['orders'])} ongoing orders. Click on 'View/Hide Orders' to see order details.")
			
		if ss.orders_full:
			st.write("WARNING: Customer order cancelled. You are processing the maximum number of concurrent orders. Complete more orders.")
			
	with col2:
		
		view_request = st.button('View/Hide Current Orders', on_click=switch_orders_display)

		if ss.display_orders:
			st.write('Current Orders')
			st.write(ss.group_state['orders'])
	
	if path.isfile(ss.filepath+'parts_selction.csv'):
	    st.header(":blue[Mechanical Engineer]")
	    st.markdown("Parts, materials, and manufacturing processes selected by the :blue[Mechanical Engineer]")
	    selection_df = pd.read_csv(ss.filepath+'parts_selction.csv')
	    selection_df.index = list(range(1, len(selection_df)+1))
	    st.dataframe(selection_df, width=3000)
	
	if path.isfile(ss.filepath+'parts_material_process_justification.csv'):
	    st.markdown("Justifications of the :blue[Mechanical Engineer]")
	    just_df = pd.read_csv(ss.filepath+'parts_material_process_justification.csv')
	    just_df.index = list(range(1, len(just_df)+1))
	    st.dataframe(just_df, width=3000)
	
def feedback():
	
	text = ""
	if path.isfile(ss.filepath+'fb_pm_m.txt'):
	    with open(ss.filepath+'fb_pm_m.txt', 'r') as f:
	        text = f.read()
	
	fb_pm_m = st.text_area("Your feedback to the Mechanical Engineer", text)
	if fb_pm_m != "":
	    with open(ss.filepath+"fb_pm_m.txt", "w") as f:
	        f.write(fb_pm_m)
	    st.markdown("---")
	
	if st.button('Clear Feedback', key=0):
	    if path.isfile(ss.filepath+'fb_pm_m.txt'):
	        os.remove(ss.filepath+'fb_pm_m.txt')
	
	if path.isfile(ss.filepath+'orders.csv'):
	    st.header(":blue[Industrial Engineer]")
	    st.markdown("Orders by the :blue[Industrial Engineer]")
	    orders_df = pd.read_csv(ss.filepath+'orders.csv')
	    orders_df.index = list(range(1, len(orders_df)+1))
	    st.dataframe(orders_df, width=3000)
	
	text = ""
	if path.isfile(ss.filepath+'fb_pm_i.txt'):
	    with open(ss.filepath+'fb_pm_i.txt', 'r') as f:
	        text = f.read()
	
	fb_pm_i = st.text_area("Your feedback to the Industrial Engineer", text)
	if fb_pm_i != "":
	    with open(ss.filepath+"fb_pm_i.txt", "w") as f:
	        f.write(fb_pm_i)
	
	if st.button('Clear Feedback', key=1):
	    if path.isfile(ss.filepath+'fb_pm_i.txt'):
	        os.remove(ss.filepath+'fb_pm_i.txt')
	
	st.markdown("---")
	text = ""
	if path.isfile(ss.filepath+'fb_pm_pum.txt'):
	    with open(ss.filepath+'fb_pm_pum.txt', 'r') as f:
	        text = f.read()
	
	fb_pm_pum = st.text_area("Your feedback to the Purchasing Manager", text)
	if fb_pm_pum != "":
	    with open(ss.filepath+"fb_pm_pum.txt", "w") as f:
	        f.write(fb_pm_pum)
	    st.markdown("---")
	
	if st.button('Clear Feedback', key=2):
	    if path.isfile(ss.filepath+'fb_pm_pum.txt'):
	        os.remove(ss.filepath+'fb_pm_pum.txt')
	
	
	st.markdown("---")
	text = ""
	if path.isfile(ss.filepath+'fb_pm_d.txt'):
	    with open(ss.filepath+'fb_pm_d.txt', 'r') as f:
	        text = f.read()
	
	fb_pm_d = st.text_area("Your feedback to the Design Engineer", text)
	if fb_pm_d != "":
	    with open(ss.filepath+"fb_pm_d.txt", "w") as f:
	        f.write(fb_pm_d)
	    st.markdown("---")
	
	if st.button('Clear Feedback', key=3):
	    if path.isfile(ss.filepath+'fb_pm_d.txt'):
	        os.remove(ss.filepath+'fb_pm_d.txt')

def create_order():
		
	if len(ss.group_state['orders']) < ss.order_limit:
		group.add_new_order(ss.group)
		ss.order_requested = True
		ss.orders_full = False
	else:
		ss.order_requested = False
		ss.orders_full = True
	
def switch_orders_display():
	if ss.display_orders == True:
		ss.display_orders = False
	else:
		ss.display_orders = True