import streamlit as st
import controller.controller as control


def display():
    """Display the page "Panier" in the streamlit app."""

    # Request to the DB
    test_id_user = 2
    shopping_cart = control.user_shopping_cart("ecommerce_database", test_id_user)

    # Display the title
    st.header("Panier")

    # Display the shopping cart as a table
    column_widths = [1, 3, 2, 1, 1, 1]
    display_table_header(column_widths)
    total_price_ET, total_price_IT = 0, 0
    for command_line in shopping_cart:
        add_prices = display_table_line(column_widths, command_line)
        total_price_ET += add_prices[0]
        total_price_IT += add_prices[1]

    # Display the order button and the total price
    column_widths = [4, 2]
    display_order_and_total(column_widths, total_price_ET, total_price_IT)


def display_table_header(column_widths: list[int]):
    """Display the shopping cart table header

    Args:
        column_widths (list[int]): Relative widths for each column
    """
    # Dividing the field into columns
    (
        col_image,
        col_name,
        col_quantity,
        col_price_ET,
        col_total_price_ET,
        col_total_price_IT,
    ) = st.columns(column_widths)

    # Column image
    with col_image:
        st.text("Image")

    # Column product name
    with col_name:
        st.text("Nom du produit")

    # Column quantity in the shopping cart
    with col_quantity:
        st.text("Quantité")

    # Column product price
    with col_price_ET:
        st.text("Prix HT unitaire")

    # Column command line price
    with col_total_price_ET:
        st.text("Prix HT")

    # Column command line price
    with col_total_price_IT:
        st.text("Prix TTC")


def display_table_line(column_widths: list[int], command_line: dict) -> tuple[int, int]:
    """Display a command line of the shopping cart.

    Args:
        column_widths (list[int]): Relative widths of the columns
        command_line (dict): The command line information

    Returns:
        int: The total cost for this command line
    """
    # Dividing the field into columns
    (
        col_image,
        col_name,
        col_quantity,
        col_price_ET,
        col_total_price_ET,
        col_total_price_IT,
    ) = st.columns(column_widths, vertical_alignment="center")

    # Column image
    with col_image:
        st.image(command_line["image_path"], width=50)

    # Column product name
    with col_name:
        st.text(command_line["product_name"])

    # Column quantity in the shopping cart
    with col_quantity:
        new_quantity = st.number_input(
            command_line["product_name"] + "_quantity",
            min_value=0,
            max_value=command_line["number_of_units"],
            value=command_line["quantity"],
            step=1,
            label_visibility="collapsed",
        )
        if new_quantity != command_line["quantity"]:
            control.update_command_line(
                "ecommerce_database",
                command_line["id_prod"],
                command_line["id_shoppingcart"],
                new_quantity,
            )
            st.rerun()

    # Column product price ET
    with col_price_ET:
        st.text(f"{command_line["price_ET"]:10.2f} €")

    # Column command line price ET
    with col_total_price_ET:
        total_price_ET = command_line["price_ET"] * command_line["quantity"]
        st.text(f"{total_price_ET:10.2f} €")

    # Column command line price IT
    with col_total_price_IT:
        total_price_IT = total_price_ET * (1 + command_line["rate_vat"])
        st.text(
            f"{total_price_IT:10.2f} €"
        )

    return total_price_ET, total_price_IT


def display_order_and_total(
    column_widths: list[int], total_price: int, total_price_vat: int
):
    """Display the order button and the total cost of the shopping cart

    Args:
        column_widths (list[int]): Relative widths of the columns
        total_price (int): Total cost of the shopping cart
    """
    # Dividing the field into columns
    empty_col, col_total_price = st.columns(
        column_widths, vertical_alignment="bottom"
    )

    with col_total_price:
        st.text(
            f"Prix total HT: {total_price:10.2f} €\nPrix total TTC: {total_price_vat:10.2f} €"
        )
        st.button("order", icon="🚴")


if __name__ == "__main__":
    display()
