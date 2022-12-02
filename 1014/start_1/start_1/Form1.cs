using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace start_1
{
    public partial class Form1 : Form
    {
        Dictionary<string, string> micNames;
        public Form1()
        {
            InitializeComponent();

            this.micNames = new Dictionary<string, string>();

            this.micNames.Add("マイク1", "1");
            this.micNames.Add("マイク2", "2");

            foreach (KeyValuePair<string, string> data in this.micNames)
            {
                micBox.Items.Add(data.Key);
            }
        }

        private void micSelected(object sender, EventArgs e)
        {

        }

        private void ExitMenueClicked(object sender, EventArgs e)
        {
            this.Close();
        }
    }
}
