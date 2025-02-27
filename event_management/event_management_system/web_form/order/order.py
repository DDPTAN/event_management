import frappe

@frappe.whitelist()
def return_event_tickets(order_id):
    order = frappe.get_doc('Orders', order_id)
    if order.event_id and order.total_ticket:
        event = frappe.get_doc('Events', order.event_id)
        # Tambahkan kembali jumlah tiket yang tersedia
        event.number_of_tickets += order.total_ticket
        event.save()
        order.status = "Cancelled"
        order.save()
        # Kembalikan pesan sukses
        return "success"
    else:
        # Kembalikan pesan error jika tidak berhasil
        return "failed"

def get_context(context):
    # Ambil ID dari pesanan yang sedang diedit
    order_id = frappe.form_dict.get('name')
    # Dapatkan path URL saat ini
    current_url = frappe.local.request.path
    # Dapatkan user dan roles
    user = frappe.session.user
    
    # Periksa user type
    user_type = frappe.get_value("User", user, "user_type")
    
    if order_id:
        order = frappe.get_doc('Orders', order_id)

        # Periksa apakah URL adalah halaman edit
        if "edit" in current_url and order.status in ["Confirmed", "Cancelled"]:
            # Redirect pengguna ke halaman detail pesanan
            frappe.local.flags.redirect_location = f"/admin/order/{order_id}"
            raise frappe.Redirect

    # Periksa jika role adalah Event Participant
    if "/admin/event" in current_url or "/admin/order" in current_url:
        # Jika user adalah 'Website User', redirect ke dashboard
        if user_type == "Website User":
            frappe.local.flags.redirect_location = "/dashboard"
            raise frappe.Redirect
    
    # Periksa use belum login
    if "Guest" in user:
        frappe.local.flags.redirect_location = f"/login"
        raise frappe.Redirect
    pass
