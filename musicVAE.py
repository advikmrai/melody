print('Copying checkpoint from GCS. This will take less than a minute...')
# This will download the mel_2bar_big checkpoint
# See the list of checkpoints: https://github.com/magenta/magenta/tree/master/magenta/models/music_vae#pre-trained-checkpoints
!gsutil -q -m cp -R gs://download.magenta.tensorflow.org/models/music_vae/colab2/checkpoints/mel_2bar_big.ckpt.* /content/

# Import dependencies
from magenta.models.music_vae import configs
from magenta.models.music_vae.trained_model import TrainedModel

# Initialize the model
print("Initializing Music VAE...")
music_vae = TrainedModel(
      configs.CONFIG_MAP['cat-mel_2bar_big'], 
      batch_size=4, 
      checkpoint_dir_or_path='/content/mel_2bar_big.ckpt')

print('🎉 Done!')

generated_sequences = music_vae.sample(n=2, length=80, temperature=1.0)

for ns in generated_sequences:
  # print(ns)
  note_seq.plot_sequence(ns)
  note_seq.play_sequence(ns, synth=note_seq.fluidsynth)

# We're going to interpolate between the Twinkle Twinkle Little Star
# NoteSequence we defined in the first section, and one of the generated
# sequences from the previous VAE example

# How many sequences, including the start and end ones, to generate.
num_steps = 8;

# This gives us a list of sequences.
note_sequences = music_vae.interpolate(
      twinkle_twinkle,
      teapot, 
      num_steps=num_steps,
      length=32)

# Concatenate them into one long sequence, with the start and 
# end sequences at each end. 
interp_seq = note_seq.sequences_lib.concatenate_sequences(note_sequences)

note_seq.play_sequence(interp_seq, synth=note_seq.fluidsynth)
note_seq.plot_sequence(interp_seq)
