using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApp2
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void calcClicked(object sender, EventArgs e)
        {
            int price;
            bool success = int.TryParse(this.priceBOX.Text, out price);

            if (success)
            {
                int taxPrice = (int)(price * 1.1);
                this.taxPriceBOX.Text = taxPrice.ToString();
            }
        }
    }
}
