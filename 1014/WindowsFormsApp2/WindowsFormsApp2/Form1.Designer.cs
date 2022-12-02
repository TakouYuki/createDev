namespace WindowsFormsApp2
{
    partial class Form1
    {
        /// <summary>
        /// 必要なデザイナー変数です。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 使用中のリソースをすべてクリーンアップします。
        /// </summary>
        /// <param name="disposing">マネージド リソースを破棄する場合は true を指定し、その他の場合は false を指定します。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows フォーム デザイナーで生成されたコード

        /// <summary>
        /// デザイナー サポートに必要なメソッドです。このメソッドの内容を
        /// コード エディターで変更しないでください。
        /// </summary>
        private void InitializeComponent()
        {
            this.priceBOX = new System.Windows.Forms.TextBox();
            this.taxPriceBOX = new System.Windows.Forms.TextBox();
            this.calc = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // priceBOX
            // 
            this.priceBOX.Location = new System.Drawing.Point(344, 139);
            this.priceBOX.Name = "priceBOX";
            this.priceBOX.Size = new System.Drawing.Size(497, 19);
            this.priceBOX.TabIndex = 0;
            // 
            // taxPriceBOX
            // 
            this.taxPriceBOX.Enabled = false;
            this.taxPriceBOX.Location = new System.Drawing.Point(344, 208);
            this.taxPriceBOX.Name = "taxPriceBOX";
            this.taxPriceBOX.Size = new System.Drawing.Size(497, 19);
            this.taxPriceBOX.TabIndex = 1;
            // 
            // calc
            // 
            this.calc.Location = new System.Drawing.Point(723, 276);
            this.calc.Name = "calc";
            this.calc.Size = new System.Drawing.Size(118, 23);
            this.calc.TabIndex = 2;
            this.calc.Text = "税込んでみる。";
            this.calc.UseVisualStyleBackColor = true;
            this.calc.Click += new System.EventHandler(this.calcClicked);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(231, 142);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(53, 12);
            this.label1.TabIndex = 3;
            this.label1.Text = "税抜価格";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(231, 211);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(64, 12);
            this.label2.TabIndex = 4;
            this.label2.Text = "税込み価格";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1182, 530);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.calc);
            this.Controls.Add(this.taxPriceBOX);
            this.Controls.Add(this.priceBOX);
            this.Name = "Form1";
            this.Text = "Form1";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox priceBOX;
        private System.Windows.Forms.TextBox taxPriceBOX;
        private System.Windows.Forms.Button calc;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
    }
}

