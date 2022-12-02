using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using NAudio.Wave;
using NAudio.Codecs;
using NAudio.CoreAudioApi;

using System.Collections;
using System.Threading;


namespace start_1
{
    public partial class Form3 : Form
    {
        Form1 form1;

        WaveInEvent waveIn;
        WaveFileWriter waveWriter;
        //public WaveIn waveSource = null;
        //public WaveFileWriter waveFile = null;

        public Form3(Form1 form1)
        {
            InitializeComponent();
            this.form1 = form1;
            MMDeviceEnumerator enumerator = new MMDeviceEnumerator();
            var devices = enumerator.EnumerateAudioEndPoints(DataFlow.All, DeviceState.Active);
            form1.comboBox1.Items.AddRange(devices.ToArray());
        }

        public Form3()
        {
            InitializeComponent();
        }

        private void ExitMenueClicked(object sender, EventArgs e)
        {
        
        }

        private void 終了ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            //初期画面の表示
            Form1 f1 = new Form1();
            f1.Visible = true;

            //現在画面を閉じる
            this.Close();
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            if (form1.comboBox1.SelectedItem != null)
            {
                var device = (MMDevice)form1.comboBox1.SelectedItem;
                progressBar1.Value = (int)(Math.Round(device.AudioMeterInformation.MasterPeakValue * 100));
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            // 録音デバイスを選びたい場合は、WaveInEvent.DeviceCount、WaveInEvent.GetCapabilities を使って探してください。
            var deviceNumber = 0;

            // 録画処理を開始
            // WaveIn だと、「System.InvalidOperationException: 'Use WaveInEvent to record on a background thread'」のエラーが発生する
            // waveIn = new WaveIn();
            waveIn = new WaveInEvent();
            waveIn.DeviceNumber = deviceNumber;
            waveIn.WaveFormat = new WaveFormat(44100, WaveIn.GetCapabilities(deviceNumber).Channels);

            waveWriter = new WaveFileWriter("z:\\audiotest\\test1.wav", waveIn.WaveFormat);

            waveIn.DataAvailable += (_, ee) =>
            {
                waveWriter.Write(ee.Buffer, 0, ee.BytesRecorded);
                waveWriter.Flush();
            };
            waveIn.RecordingStopped += (_, __) =>
            {
                waveWriter.Dispose();
                waveWriter = null;
                waveIn.Dispose();
            };

            waveIn.StartRecording();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            waveIn.StopRecording();

            
        }
    }
}
