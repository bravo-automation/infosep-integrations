import pandas as pd

class CustomExcelGenerator():
    def __init__(self, data, output_file="output.xlsx", column_mapping=None, desired_order=None, auto_adjust=None, auto_filter=False, generic_excel=False):
        self.data = data
        self.output_file = output_file
        self.column_mapping = column_mapping
        self.desired_order = desired_order
        self.auto_adjust = auto_adjust
        self.auto_filter = auto_filter
        self.generic_excel = generic_excel

    def set_auto_adjust(self, df, worksheet):
        if self.auto_adjust is None:
            # Auto-adjust column width
            for i, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).map(len).max(),  # Length of the longest data in the column
                    len(col)  # Length of the column header
                )
                worksheet.set_column(i, i, max_length + 2)  # Add some padding
        else:
            for i, col in enumerate(df.columns):
                if col in self.auto_adjust:
                    max_length = max(
                        df[col].astype(str).map(len).max(),  # Length of the longest data in the column
                        len(col)  # Length of the column header
                    )
                    worksheet.set_column(i, i, max_length + 2)  # Add some padding

    def dict_to_excel(self):
        try:
            df = pd.DataFrame.from_dict(self.data)
            if self.column_mapping is not None:
                df.rename(columns=self.column_mapping, inplace=True)

            # Reorder columns as needed
            if self.desired_order is not None:
                desired_order = self.desired_order
                df = df[desired_order]

            writer = pd.ExcelWriter(self.output_file, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1', index=False)
            workbook  = writer.book
            worksheet = writer.sheets['Sheet1']

            self.set_auto_adjust(df, worksheet)

            white_format = workbook.add_format({'bg_color': '#FFFFFF', 'border_color': '#646464', 'align': 'center','valign': 'vcenter', 'border': 1})

            header_format = workbook.add_format({'bold': True,
                                                'text_wrap': True, 
                                                'align': 'center',
                                                'valign': 'vcenter',
                                                'bg_color': '#008080',
                                                'font_color': '#ffffff',
                                                'border': 1,
                                                'border_color': '#646464'})
            pn_price_format = workbook.add_format({'align': 'center',
                                                'valign': 'vcenter',
                                                'font_color': '#008080'})

            # Apply header format
            worksheet.conditional_format(0, 0, 0, len(df.columns) - 1, {'type': 'no_blanks', 'format': header_format})

            # Apply white format to the entire table (excluding the header)
            last_row = len(df) + 1  # +1 to account for the header row
            worksheet.conditional_format(1, 0, last_row, len(df.columns) - 1, {
                'type': 'no_blanks',
                'format': white_format
            })

            if not self.generic_excel:
            # Apply PN and PRICE column formatting
                pn_col_index = df.columns.get_loc("PN")
                price_col_index = df.columns.get_loc("TG_PRICE")
                
                pn_max_length = max(df["PN"].astype(str).map(len).max(), len("PN"))
                price_max_length = max(df["TG_PRICE"].astype(str).map(len).max(), len("TG_PRICE"))

                worksheet.set_column(pn_col_index, pn_col_index, pn_max_length + 2, pn_price_format)
                worksheet.set_column(price_col_index, price_col_index, price_max_length + 2, pn_price_format)

            # Add autofilter to the first row
            if self.auto_filter:
                worksheet.autofilter(0, 0, 0, len(df.columns) - 1)

            writer._save()
            print(f"Excel file saved successfully at: {self.output_file}")
        except Exception as e:
            print(f"An error occurred: {e}")
